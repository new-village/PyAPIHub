# api/endpoints/keiba.py
from fastapi import APIRouter, HTTPException
import pickle
import os
import json
from typing import List, Dict
import pandas as pd
import keibascraper
import lightgbm as lgm

router = APIRouter()

@router.get("/entry/{race_id}")
async def get_entry(race_id: str):
    """
    指定されたレースIDに基づいて出走記録を取得します。

    - **race_id**: 12桁の数値文字列
    """    
    try:
        # keibascraper.load を使用して出走記録を取得
        race_info = keibascraper.load("entry", race_id)
        odds_info = keibascraper.load('odds', race_id)
        race = merge_race_and_odds(race_info, odds_info)
        race = pd.read_json(json.dumps(race))
        entry = pd.json_normalize(race['entry'])
        race = race.reset_index(drop=True)  # Reset index of race DataFrame
        race.drop(['id', 'entry', 'race_time'], axis=1, inplace=True)
        df = pd.concat([race, entry], axis=1)
        df.set_index('id', inplace=True)

        td = df.select_dtypes(exclude=object)
        td = td.astype(float)

        model = load_model("/data/model/keiba.model")
        # 予測の実行
        df['pred_score'] = model.predict(td)
        df['pred_rank'] = df.groupby('race_id')['pred_score'].rank(method='first', ascending=True)
        df = df.sort_values('pred_rank')

        # 取得したデータをそのまま返す
        return json.loads(df.to_json(orient='records'))

    except keibascraper.KeibaScraperError as e:
        # keibascraper 独自のエラーが発生した場合
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        # その他の予期しないエラー
        raise HTTPException(status_code=500, detail="Internal Server Error.")


def merge_race_and_odds(race: Dict, odds: List[Dict]) -> Dict:
    """
    Merges race data with odds data based on matching 'id' fields.

    Parameters:
        race (Dict): The first dataset containing race information with an "entry" key.
        odds (List[Dict]): The second dataset containing odds information, each with an "id" key.

    Returns:
        Dict: The merged race data.
    """
    if 'entry' not in race:
        raise ValueError("The race data does not contain 'entry' key.")

    # Create a dictionary for quick lookup of odds by 'id'
    odds_lookup = {item['id']: item for item in odds if 'id' in item}

    merged_entries = []
    for entry in race.get('entry', []):
        entry_id = entry.get('id')
        if not entry_id:
            print("An entry in race data does not have an 'id' key. Entry skipped.")
            continue

        if entry_id in odds_lookup:
            # Merge the two dictionaries. Odds data values will overwrite race data if keys overlap.
            merged_entry = {**entry, **odds_lookup[entry_id]}
            merged_entries.append(merged_entry)
        else:
            # If no matching odds data, keep the entry as is
            print(f"No matching odds data for entry ID {entry_id}. Entry added without merging.")
            merged_entries.append(entry)

    # Update the race data with merged entries
    race["entry"] = merged_entries
    return race

def load_model(model_path='/data/model/keiba.model'):
    """
    指定されたパスからピクルス化されたモデルをロードします。

    Args:
        model_path (str): モデルファイルのパス。

    Returns:
        model: デシリアライズされた機械学習モデル。
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"モデルファイルが見つかりません: {model_path}")
    
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except pickle.UnpicklingError:
        raise Exception("モデルのデシリアライズ中にエラーが発生しました。")
    except Exception as e:
        raise Exception(f"モデルのロード中に予期しないエラーが発生しました: {e}")

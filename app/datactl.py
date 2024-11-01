import pandas as pd
import numpy as np

DF = pd.read_csv("./app/src/의약품안전사용서비스(DUR)_병용금기 품목리스트 2020.9.csv", encoding="cp949")
#DF = pd.read_csv("./medical_hyun/app/src/의약품안전사용서비스(DUR)_병용금기 품목리스트 2020.9.csv", encoding="cp949")

column_to_use = ["제품명A", "업체명A", "고시일자", "성분명A"]
DF["고시일자"] = pd.to_datetime(DF["고시일자"], errors='coerce')
DF = DF[column_to_use]

def get_company_columns():
    result = DF["업체명A"].unique().tolist()  # JSON 형식으로 리스트 변환
    return result

# 업체 - 성분
def get_ingredient(company=None, start_date="2004-01-16", end_date="2020-07-10"):
    filtered_columns = ["업체명A", "성분명A", "고시일자"]

    # 날짜 필터링
    filtered_df = DF[(DF["고시일자"] >= start_date) & (DF["고시일자"] <= end_date)]
    filtered_df = filtered_df[filtered_columns]

    # 회사 필터링
    if company is None:
        company = filtered_df['업체명A'].unique()
    else:
        company = [company]

    count_result = []
    time_result = []

    for company_column in company:
        temp_df = filtered_df[filtered_df["업체명A"] == company_column]

        # 성분별 카운트 데이터 생성
        ingredient_counts = temp_df["성분명A"].value_counts().reset_index()
        ingredient_counts.columns = ['ingredient', 'count']

        # 카운트 결과 추가
        count_result.append({
            "company": company_column,
            "data": {
                "ingredient": ingredient_counts['ingredient'].tolist(),
                "count": ingredient_counts['count'].tolist()
            }
        })

        # 시계열 데이터 생성
        all_periods = pd.date_range(start=start_date, end=end_date, freq='ME').to_period("M")
        time_group = temp_df.groupby([temp_df["고시일자"].dt.to_period("M"), "성분명A"]).size()

        all_index = pd.MultiIndex.from_product([all_periods, time_group.index.get_level_values(1).unique()],
                                               names=["고시일자", "성분명A"])
        time_group = time_group.reindex(all_index, fill_value=0)
        cumulative_time_group = time_group.groupby(level=1).cumsum()

        cumulative_df = cumulative_time_group.reset_index(name='누적개수')
        cumulative_df['고시일자'] = cumulative_df['고시일자'].astype(str)

        # 시계열 데이터 포맷팅
        for ingredient in cumulative_df['성분명A'].unique():
            ingredient_data = cumulative_df[cumulative_df['성분명A'] == ingredient]
            time_result.append({
                "company": company_column,
                "ingredient": ingredient,
                "data": {
                    "time": ingredient_data['고시일자'].tolist(),
                    "count": ingredient_data['누적개수'].tolist()
                }
            })

    result = {"count_result": count_result, "time_result": time_result}
    return result





# 업체 - 품목
def get_product(company=None, start_date="2004-01-16", end_date="2020-07-10"):
    filtered_columns = ["업체명A", "제품명A", "고시일자"]

    # 날짜 필터링
    filtered_df = DF[(DF["고시일자"] >= start_date) & (DF["고시일자"] <= end_date)]
    filtered_df = filtered_df[filtered_columns]

    # 회사 필터링
    if company is None:
        company = filtered_df['업체명A'].unique()
    else:
        company = [company]

    count_result = []
    time_result = []

    for company_column in company:
        temp_df = filtered_df[filtered_df["업체명A"] == company_column]
        
        # 제품별 카운트 데이터 생성
        product_counts = temp_df["제품명A"].value_counts().reset_index()
        product_counts.columns = ['product', 'count']

        # 카운트 결과 추가
        count_result.append({
            "company": company_column,
            "data": {
                "product": product_counts['product'].tolist(),
                "count": product_counts['count'].tolist()
            }
        })
    
        # 시계열 데이터 생성
        all_periods = pd.date_range(start=start_date, end=end_date, freq='ME').to_period("M")
        time_group = temp_df.groupby([temp_df["고시일자"].dt.to_period("M"), "제품명A"]).size()

        all_index = pd.MultiIndex.from_product([all_periods, time_group.index.get_level_values(1).unique()],
                                               names=["고시일자", "제품명A"])
        time_group = time_group.reindex(all_index, fill_value=0)
        cumulative_time_group = time_group.groupby(level=1).cumsum()

        cumulative_df = cumulative_time_group.reset_index(name='누적개수')
        cumulative_df['고시일자'] = cumulative_df['고시일자'].astype(str)

        # 시계열 데이터 포맷팅
        for product in cumulative_df['제품명A'].unique():
            product_data = cumulative_df[cumulative_df['제품명A'] == product]
            time_result.append({
                "company": company_column,
                "product": product,
                "data": {
                    "time": product_data['고시일자'].tolist(),
                    "count": product_data['누적개수'].tolist()
                }
            })

    result = {"count_result": count_result, "time_result": time_result}
    return result


# 전체 요약
def get_all(start_date="2004-01-16", end_date="2020-07-10"):
    filtered_columns = ["업체명A", "제품명A", "성분명A", "고시일자"]

    # 날짜 필터링
    filtered_df = DF[(DF["고시일자"] >= start_date) & (DF["고시일자"] <= end_date)]
    filtered_df = filtered_df[filtered_columns]

    all_periods = pd.date_range(start=start_date, end=end_date, freq='ME').to_period("M")

    # 카운트 초기화
    ingredient_count = pd.Series(0, index=all_periods, name="누적성분개수")
    product_count = pd.Series(0, index=all_periods, name="누적제품개수")
    company_count = pd.Series(0, index=all_periods, name="누적업체개수")

    # 성분별 카운트 계산
    ingredient_time_group = filtered_df.groupby(filtered_df["고시일자"].dt.to_period("M"))["성분명A"].nunique()
    ingredient_count = ingredient_time_group.reindex(all_periods, fill_value=0).cumsum()

    # 제품별 카운트 계산
    product_time_group = filtered_df.groupby(filtered_df["고시일자"].dt.to_period("M"))["제품명A"].nunique()
    product_count = product_time_group.reindex(all_periods, fill_value=0).cumsum()

    # 업체별 카운트 계산
    company_time_group = filtered_df.groupby(filtered_df["고시일자"].dt.to_period("M"))["업체명A"].nunique()
    company_count = company_time_group.reindex(all_periods, fill_value=0).cumsum()

    # 최종 결과 구성
    result = {
        "ingredient_count": {
            "ingredient": filtered_df["성분명A"].unique().tolist(),
            "count": ingredient_count.tolist()
        },
        "product_count": {
            "product": filtered_df["제품명A"].unique().tolist(),
            "count": product_count.tolist()
        },
        "company_count": {
            "company": filtered_df["업체명A"].unique().tolist(),
            "count": company_count.tolist()
        }
    }
    
    return result


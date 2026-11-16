"""자신의 심화 구현을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
# 파일 경로 관리 기능 사용
# - Path : 파일 및 디렉터리 경로 조작
from pathlib import Path
# 시스템 제어 및 경로 추가 기능 사용
# - sys : 파이썬 런타임 환경 제어
import sys
# JSON 데이터 직렬화 및 역직렬화 기능 사용
# - json : JSON 데이터 처리
import json
# 단위 테스트 프레임워크 기능 사용
# - pytest : 파이썬 테스트 실행 및 예외/파라미터화 검증
import pytest
# 현재 파일 기준 상위 경로 설정
# - HERE : 상위 디렉터리 경로
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
# 코스킷 입출력 기능 사용
# - DATA : 데이터 저장 경로
# - read_json : JSON 파일 읽기 함수
from coursekit.io import DATA, read_json
# 컨텍스트 빌더 기능 사용
# - select_context : 컨텍스트 선택 함수
# - calculate_budget : 토큰 예산 계산 함수
from context_builder import select_context, calculate_budget

"""컨텍스트 선택 순서 유지 및 토큰 예산 계산 결과가 올바른지 검증하는 테스트 함수"""

# 순서 및 예산 검증 테스트
def test_order_and_budget():
    # 전체 지식 데이터 로드
    # - knowledge_v1.json 파일 읽기
    rows=read_json(DATA/"knowledge_v1.json")
    # 중복 ID가 포함된 지식 선택 및 JSON 직렬화 수행
    # - [102, 102, 101] 입력
    chosen,text=select_context(rows,[102,102,101])
    # 선택된 항목의 ID 순서가 [102, 101]로 유지되는지 검증
    assert [x["id"] for x in chosen]==[102,101]
    # 직렬화된 텍스트가 chosen 데이터와 일치하는지 검증
    assert json.loads(text)==chosen
    # 가상 토큰 예산의 가용 공간이 4936인지 검증
    assert calculate_budget()["available_for_context"]==4936

"""스냅샷 데이터에 중복이 있거나 존재하지 않는 ID가 입력되었을 때 예외가 발생하는지 검증하는 파라미터화 테스트 함수"""

# 유효하지 않은 스냅샷 검증 테스트 (파라미터화)
# - mode : "missing" 또는 "duplicate" 모드 전달
@pytest.mark.parametrize("mode",["missing","duplicate"])
def test_invalid_snapshot(mode):
    # 전체 지식 데이터 로드
    # - knowledge_v1.json 파일 읽기
    rows=read_json(DATA/"knowledge_v1.json")
    # ValueError 예외 발생 여부 검증
    with pytest.raises(ValueError):
        # mode가 duplicate인 경우 중복 스냅샷 생성, missing인 경우 존재하지 않는 ID [999] 전달
        select_context(rows+[rows[0]] if mode=="duplicate" else rows,[999] if mode=="missing" else [101])

"""
본 테스트 코드는 작성된 컨텍스트 빌더의 핵심 기능인 순서 보존, 중복 제거, 예산 산출의 정확성뿐만 아니라,
잘못된 데이터(누락된 ID, 스냅샷 중복) 입력 시 ValueError 예외가 올바르게 발생하는지 엄격하게 검증하도록 구현하였다.
"""
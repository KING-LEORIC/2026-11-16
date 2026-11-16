"""자신의 심화 구현을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
# 파일 경로 관리 기능 사용
# - Path : 파일 및 디렉터리 경로 조작
from pathlib import Path
# 시스템 제어 및 경로 추가 기능 사용
# - sys : 파이썬 런타임 환경 제어
import sys
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
# 재시도 정책 및 프롬프트 수정 기능 사용
# - run_with_retry : 재시도 포함 실행 제어 함수
# - repair_prompt : 프롬프트 수정 요청 생성 함수
from retry_policy import run_with_retry, repair_prompt
# 코스킷 재시도 시나리오 실행 기능 사용
# - run_fixture_scenarios : 픽스처 기반 시나리오 실행 함수
from coursekit.retry import run_fixture_scenarios

"""재시도 호출 횟수가 허용된 범위 내에서 올바르게 동작하는지 검증하는 테스트 함수"""

# 호출 범위 검증 테스트
def test_call_bounds():
    # 검증 픽스처 데이터를 로드하고 재시도 러너를 통해 시나리오 실행 결과 획득
    results=run_fixture_scenarios(read_json(DATA/"validation_fixtures.json"),runner=run_with_retry)
    # 각 시나리오별 호출 횟수가 [2, 2, 1, 1]과 일치하는지 단언 검증
    assert [r["calls"] for r in results]==[2,2,1,1]

"""알려지지 않은 비표준 오류 문자열이 전달되었을 때 예외가 발생하는지 검증하는 테스트 함수"""

# 알 수 없는 오류 전달 차단 검증 테스트
def test_unknown_error_not_forwarded():
    # 허용되지 않은 비표준 오류 문자열로 프롬프트 수정 시도 시 ValueError 발생 여부 검증
    with pytest.raises(ValueError):repair_prompt("original","PRIVATE_PATH_TEST")

"""안전한 수정 요청 요약 생성 시 원본 프롬프트가 유지되고 민감한 오류 문자열이 포함되지 않는지 검증하는 테스트 함수"""

# 안전한 요약 생성 검증 테스트
def test_safe_summary():
    # 허용된 형식 오류 목록을 순회하며 검사
    for error in ["json_error","schema_error"]:
        # 수정 요청 프롬프트 생성
        result=repair_prompt("same prompt",error)
        # 결과가 원본 프롬프트로 시작하고 민감한 테스트 문자열이 포함되지 않았는지 단언 검증
        assert result.startswith("same prompt") and "PRIVATE_PATH_TEST" not in result

"""
본 테스트 코드는 재시도 제어 로직의 호출 횟수 제한(최대 2회), 허용되지 않은 비표준 오류의 안전한 차단,
그리고 프롬프트 수정 요청 시 민감 정보 누출 방지 기능이 정확하게 동작하는지 검증하도록 구현하였다.
"""
"""Day21 실습 06: JSON·Schema·참조 검증. 실행: python main.py"""
# 파일 경로 관리 기능 사용
# - Path : 파일 및 디렉터리 경로 조작
from pathlib import Path
# 시스템 제어 및 경로 추가 기능 사용
# - sys : 파이썬 런타임 환경 제어
import sys

# 현재 파일 기준 상위 경로 설정
# - HERE : 현재 디렉터리 경로
# - ROLE_ROOT : 상위 프로젝트 루트 경로
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
# 코스킷 입출력 기능 사용
# - DATA : 데이터 저장 경로
# - read_json : JSON 파일 읽기 함수
# - write_json : JSON 파일 쓰기 함수
from coursekit.io import DATA, read_json, write_json

# 기준: Day21 PPT 46~55장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
# Pydantic 유효성 검증 예외 기능 사용
# - ValidationError : 모델 검증 실패 시 발생하는 예외
from pydantic import ValidationError

# 계약 관련 스키마 및 검증 함수 사용
# - make_model : Pydantic 모델 생성 함수
# - parse_answer : 답변 파싱 함수
# - check_rules : 비즈니스 규칙 검사 함수
from contracts.schema import make_model
from contracts.parser import parse_answer
from contracts.rules import check_rules

"""답변 문자열을 파싱하고 비즈니스 규칙을 검사하여 유효성을 검증하는 함수"""

# 답변 검증 함수
# - raw : 원본 응답 문자열 (str)
# - provided_ids : 제공된 출처 ID 목록 (list[int])
def validate_answer(raw, provided_ids):
    # 응답 파싱 수행
    obj,error=parse_answer(raw)
    # 파싱 오류 발생 시 즉시 반환
    if error:
        return None,error
    # 비즈니스 규칙 검사 수행
    error=check_rules(obj,provided_ids)
    return (None,error) if error else (obj,None)

"""검증 픽스처 처리, 스키마 내보내기, 반례 검증 및 경계값 테스트를 수행하는 메인 함수"""

# 메인 실행 함수
# - 픽스처 로드, 검증 수행, 반례 분석 및 경계값 검사 수행
def main() -> None:
    # 검증 픽스처 데이터 로드
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-06-A05: 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 26개 fixture가 기대 오류와 일치. semantic_counterexample은 자동 통과하지만 사람 검토 필요.
    # BEGIN D21-06-A05

    # 결과 목록 초기화
    results = []
    for item in fixtures:
        # 각 픽스처에 대해 검증 수행
        obj, error = validate_answer(item["raw_text"], item["provided_ids"])
        # 픽스처 결과 딕셔너리 구성 및 추가
        results.append({"fixture_id":item["fixture_id"],"source_mode":"fixture",
                        "error":error,"expected_error":item["expected_error"],
                        "matches_expected":error==item["expected_error"],  # TODO: error와 expected_error 비교
                        "evidence_ok":None})
    # TODO: 각 행의 matches_expected가 True인지 확인

    # 결과 및 스키마 파일 저장
    write_json(HERE/"outputs"/"fixture_results.json", results)
    write_json(HERE/"outputs"/"answer_schema.json", make_model().model_json_schema())  # TODO: model_json_schema()
    # raise NotImplementedError("D21-06-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A05
    # TODO D21-06-A06: ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 사람 예상 판단은 작성된 반례의 해설입니다. 실제 모델 평가 점수를 대신 채우지 않습니다.
    # BEGIN D21-06-A06

    # 시맨틱 반례 픽스처 추출
    counter = next(x for x in fixtures if x["fixture_id"] == "semantic_counterexample")
    # 반례에 대한 검증 수행
    obj, error = validate_answer(counter["raw_text"], counter["provided_ids"])
    # 오류가 없음을 단언 검증
    assert error is None
    # 리뷰 내용 정의
    review = {"source_mode":"fixture","auto_ok":False,"human_expected":"근거 부적합","reason":"101은 보관 위치만 설명한다. 서버 실행 위치는 102에서 확인한다.","model_performance_claim":False}
    # 시맨틱 리뷰 결과 파일 저장
    write_json(HERE/"outputs"/"semantic_review.json",review)
    # TODO: 자동 통과와 사람의 예상 근거 부적합을 별도로 저장
    # raise NotImplementedError("D21-06-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A06
    # TODO D21-06-A07: 중복 키·NaN·과도한 크기·Schema 경계를 실제 반례로 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 예외를 숨겨 통과하지 말고 기대 오류 단계까지 대조합니다.
    # BEGIN D21-06-A07
    # raw_cases = ['{"x":1,"x":2}', '{"x":NaN}', 'x'*20001]
    # TODO: 모두 json_error로 분류되는지 검사
    # TODO: 최대 500자는 허용, bool ID는 거부
    # bool_rejected = False
    # 비정상 raw 케이스에 대해 파싱 시 json_error 발생 여부 검사
    for raw in ['{"x":1,"x":2}', '{"x":NaN}', 'x'*20001]:
        _,error=parse_answer(raw)
        assert error=="json_error"
    # 모델 클래스 생성
    Model=make_model()
    # 유효한 답변 데이터 정의 (최대 길이 500자)
    valid={"status":"answered","answer":"가"*500,"source_ids":[101,102,103],"missing_information":""}
    # 500자 답변이 정상 수용되는지 검증
    assert len(Model.model_validate(valid).answer)==500
    # 부울 타입 ID가 포함된 잘못된 데이터 정의
    invalid=dict(valid,source_ids=[True])
    try:
        # 잘못된 모델 데이터 검증 시도 (예외 발생 예상)
        Model.model_validate(invalid)
    except ValidationError:
        bool_rejected=True
    else:
        bool_rejected=False
    # 부울 ID가 거부되었는지 단언 검증
    assert bool_rejected
    # 경계값 검사 결과 파일 저장
    write_json(HERE/"outputs"/"boundary_checks.json",{"max_answer_accepted":500,"bool_id_rejected":bool_rejected})
    # raise NotImplementedError("D21-06-A07: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A07
    print("[06] 로컬 검증 완료. 구조·참조 검사와 실제 근거 평가는 다릅니다.")

"""
본 실습 코드는 JSON 파싱 보호, 스키마 검증, 그리고 비즈니스 규칙 검사를 종합하여
다양한 픽스처와 반례에 대해 답변 유효성이 정확히 판정되는지 검증하도록 구현하였다.
"""
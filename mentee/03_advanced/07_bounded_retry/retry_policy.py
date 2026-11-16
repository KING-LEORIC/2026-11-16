"""Day21 실습 07: 실패 분류·최대 2회. 실행: python main.py"""
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
# 코스킷 입출력 및 해시/재시도 관련 기능 사용
# - DATA : 데이터 저장 경로
# - read_json : JSON 파일 읽기 함수
# - write_json : JSON 파일 쓰기 함수
# - sha_text : 해시 생성 함수
from coursekit.io import DATA, read_json, write_json, sha_text

# 기준: Day21 PPT 56~63장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
# 픽스처 제공자 및 재시도 시나리오 실행 함수 사용
# - FixtureProvider : 픽스처 기반 가상 모델 응답 제공자
# - run_fixture_scenarios : 픽스처 시나리오 실행 함수
from coursekit.retry import FixtureProvider, run_fixture_scenarios
# 정답 검증 함수 사용
# - validate_answer : 답변 유효성 검증 함수
from coursekit.contracts import validate_answer

"""오류 유형에 따른 안전한 수정 요청 프롬프트를 생성하는 함수"""

# 프롬프트 수정 요청 생성 함수
# - original : 원본 프롬프트 문자열 (str)
# - error : 발생한 오류 유형 문자열 (str)
def repair_prompt(original, error):
    # TODO D21-07-A01: 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: unknown_source는 자동 형식 수정 요청을 만들지 않습니다.
    # BEGIN D21-07-A01

    # 허용된 형식 오류별 안전한 수정 안내 문구 정의
    safe = {
        "json_error":"JSON 객체 하나를 코드 블록 없이 출력하세요.",    # TODO: JSON 문법/코드 블록 관련 짧은 안내
        "schema_error":"필수 필드·자료형·길이를 지키세요. source_ids는 양의 정수 목록입니다.",  # TODO: 필수 필드·자료형·길이 안내
    }
    # 허용되지 않은 오류인 경우 예외 발생
    if error not in safe:
        raise ValueError("형식 오류만 수정 요청을 만듭니다")
    # 원본 프롬프트에 안전한 수정 요청 문구 결합
    repaired = original + "\n[수정 요청] 같은 질문·지식·계약을 유지하세요. " + safe[error] + " 부족한 사실은 만들지 마세요."  # TODO: safe[error], 같은 질문·지식·계약 유지
    # 이전 원문 전체, traceback, 비밀 값은 붙이지 않습니다.
    # raise NotImplementedError("D21-07-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A01
    return repaired

"""최대 2회까지 응답 생성 및 검증을 반복하는 재시도 제어 함수"""

# 재시도 포함 실행 제어 함수
# - generate : 답변 생성 함수 (Callable)
# - prompt : 프롬프트 문자열 (str)
# - validate : 검증 함수 (Callable)
def run_with_retry(generate, prompt, validate):
    # TODO D21-07-A02: 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 호출 수가 최대 2. 정상 정보 부족도 1회에 종료.
    # 핵심: 성공 반환은 자동 구조·참조 통과일 뿐입니다. 근거를 맞게 읽었는지 사람 검토가 남습니다.
    # BEGIN D21-07-A02

    # 시도 이력 목록 초기화
    history = []
    for attempt in (1,2):
        # 모델 답변 생성 수행
        raw = generate(prompt)
        # 답변 유효성 검증 수행
        obj, error = validate(raw)
        # 시도 이력 기록 추가
        history.append({"attempt":attempt,"error":error,"raw_text":raw,"prompt_sha256":sha_text(prompt)})
        # 오류가 없는 경우 즉시 객체와 이력 반환
        if error is None:  # TODO: error is None일 때 즉시 obj, history 반환
            return obj, history
        # 형식 오류가 아니거나 2회차 시도인 경우 반복 중단
        if error not in {"json_error","schema_error"} or attempt==2:  # TODO: 형식 오류가 아니거나 2회째라면 break
            break
        # TODO: 다음 시도 전에만 repair_prompt를 호출
        # 다음 시도 전에만 repair_prompt를 호출하여 프롬프트 수정
        prompt = repair_prompt(prompt,error)
    # 최대 시도 초과 시 실패 처리 및 이력 반환
    return None,history
    # TODO: 끝까지 실패하면 None, history를 반환. 아래 raise는 완성 후 삭제합니다.
    # raise NotImplementedError("D21-07-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A02

"""재시도 시나리오 실행, 결과 집계, 종료 조건 및 보안 검사를 수행하는 메인 함수"""

# 메인 실행 함수
# - 픽스처 로드, 재시도 시나리오 실행, 결과 파일 저장 및 안전성 검증 수행
def main():
    # 검증 픽스처 데이터 로드
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-07-A03: 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 복구 성공·연속 실패·규칙 중단·부족 정상 종료 네 경우.
    # BEGIN D21-07-A03

    # 픽스처 시나리오 실행
    results = run_fixture_scenarios(fixtures, runner=run_with_retry)
    # calls = []  # TODO: results의 calls 목록
    # TODO: [2,2,1,1]과 비교

    # 호출 횟수가 [2, 2, 1, 1]인지 단언 검증
    assert [x["calls"] for x in results]==[2,2,1,1]
    # 재시도 결과 파일 저장
    write_json(HERE/"outputs"/"retry_results.json", {"source_mode":"fixture","results":results})  # TODO: results
    # raise NotImplementedError("D21-07-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A03
    # TODO D21-07-A04: 첫 응답과 재시도 후 결과를 다른 필드로 집계하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 처음 실패→나중 통과를 첫 응답 통과로 집계하지 않습니다.
    # BEGIN D21-07-A04
    
    # 첫 응답과 최종 결과 집계 목록 초기화
    rows = []
    for item in results:
        history = item["history"]
        rows.append({"scenario":item["scenario"],"first_error":history[0]["error"],"attempts":len(history),"final_auto_ok":item["auto_accepted"],"source_mode":"fixture"})
    # TODO: 첫 error, 전체 시도 수, 최종 자동 통과를 각각 기록

    # 첫 응답 대 최종 비교 결과 파일 저장
    write_json(HERE/"outputs"/"first_vs_final.json",rows)
    # raise NotImplementedError("D21-07-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A04
    # TODO D21-07-A05: 마지막 실패 뒤에는 수정 요청이 더 만들어지지 않는지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 범위는 완료된 문자열을 받은 뒤입니다. 공급자 거절·통신 재시도는 내일 다룹니다.
    # BEGIN D21-07-A05

    # 깨진 JSON 픽스처 데이터 추출
    bad = next(x["raw_text"] for x in fixtures if x["fixture_id"] == "broken_json")
    # 가상 공급자 설정 (반복 실패 유도)
    provider = FixtureProvider([bad,bad])
    # 재시도 실행 수행
    obj, history = run_with_retry(provider,"original",lambda raw:validate_answer(raw,[101]))
    # 결과 객체가 없고 호출 수가 2회인지 단언 검증
    assert obj is None and provider.calls==2
    assert len(provider.prompts)==2
    assert provider.prompts[1].count("[수정 요청]")==1
    # 종료 조건 검사 결과 파일 저장
    write_json(HERE/"outputs"/"termination.json",{"calls":provider.calls,"success_object":None})
    # TODO: 반환 None·호출 2회·마지막 뒤 새 수정 요청 없음 확인
    # raise NotImplementedError("D21-07-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A05
    # TODO D21-07-A06: 비표준 오류 문자열을 모델 지시로 복사하지 않는지 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-07-A06
    # blocked = False
    # TODO: 알려지지 않은 오류 문자열은 ValueError로 거부
    # TODO: 안전한 요약에 원문·경로 문자열이 섞이지 않는지 검사

    try:
        # 허용되지 않은 비표준 오류 문자열로 수정 요청 생성 시도 (예외 발생 예상)
        repair_prompt("original","PRIVATE_ERROR_TEST /private/path")
    except ValueError:
        blocked=True
    else:
        blocked=False
    # 예외 차단 여부 단언 검증
    assert blocked
    # 수정된 프롬프트에 민감한 오류 문자열이 포함되지 않았는지 단언 검증
    assert "PRIVATE_ERROR_TEST" not in repair_prompt("original","schema_error")
    # 수정 안전성 검사 결과 파일 저장
    write_json(HERE/"outputs"/"repair_safety.json",{"unknown_error_rejected":blocked,"raw_exception_forwarded":False})
    # raise NotImplementedError("D21-07-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-A06
    print("[07] 제어 흐름만 검증했습니다. 실제 모델 복구율은 측정하지 않았습니다.")

"""
본 실습 코드는 구조적 형식 오류(JSON 파싱 오류, 스키마 오류) 발생 시 안전한 수정 요청을 생성하고,
최대 2회까지 재시도를 수행하여 제어 흐름을 엄격하게 관리하는 로직을 구현하였다.
또한 비표준 오류에 대한 차단과 민감 정보 유출 방지 메커니즘이 올바르게 동작하는지 검증한다.
"""
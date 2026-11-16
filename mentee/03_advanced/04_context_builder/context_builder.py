"""Day21 실습 04: Context 선택·예산. 실행: python main.py"""
# 파일 경로 관리 기능 사용
# - Path : 파일 및 디렉터리 경로 조작
from pathlib import Path
# 시스템 제어 및 경로 추가 기능 사용
# - sys : 파이썬 런타임 환경 제어
import sys
# JSON 데이터 직렬화 및 역직렬화 기능 사용
# - json : JSON 데이터 처리
import json

# 현재 파일 기준 상위 경로 설정
# - HERE : 현재 디렉터리 경로
# - ROLE_ROOT : 상위 프로젝트 루트 경로
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
# 코스킷 입출력 및 해시/정규화 기능 사용
# - DATA : 데이터 저장 경로
# - read_json : JSON 파일 읽기 함수
# - write_json : JSON 파일 쓰기 함수
# - write_text : 텍스트 파일 쓰기 함수
# - canonical : 정규화 함수
# - sha_text : 해시 생성 함수
from coursekit.io import DATA, read_json, write_json, write_text, canonical, sha_text

# 기준: Day21 PPT 28~36장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

# 지식 컨텍스트 선택 함수
# - rows : 전체 지식 행 목록 (list)
# - selected_ids : 선택할 지식 ID 목록 (list)
def select_context(rows, selected_ids) -> tuple[list, str]:
    # TODO D21-04-A01: 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요.
    # 입력·대상: knowledge_v1 목록, selected_ids=[102]
    # 완료 기준: 102만 포함한 JSON. 없는 ID는 ValueError. 순서가 바뀌면 문맥도 달라집니다.
    # 핵심: ID 선택과 직렬화일 뿐 의미 검색·RAG를 구현한 것이 아닙니다.
    # BEGIN D21-04-A01

    # ID를 키로 하는 지식 딕셔너리 생성
    by_id = {row["id"]:row for row in rows}
    # 중복 ID 존재 여부 검사
    if len(by_id) != len(rows):
        raise ValueError("중복 ID를 확인하세요")
    # 중복 선택 제거 및 첫 순서 보존
    ids = list(dict.fromkeys(selected_ids))  # 중복 선택은 첫 순서만 남김
    # 존재하지 않는 ID 선택 여부 검사
    if any(i not in by_id for i in ids):
        raise ValueError("선택한 ID가 없습니다")
    # 선택된 지식 목록 초기화
    chosen = []
    for knowledge_id in ids:
        # 선택된 ID의 지식 항목 추가
        chosen.append(by_id[knowledge_id])  # TODO: by_id[knowledge_id]
    # 선택된 지식을 JSON 문자열로 직렬화
    context_json = json.dumps([], ensure_ascii=False)  # TODO: chosen
    # raise NotImplementedError("D21-04-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A01
    return chosen, context_json

# 토큰 예산 계산 함수
def calculate_budget() -> dict:
    # TODO D21-04-A02: PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: available_for_context=4936
    # 핵심: 실제 모델 최대 길이나 측정 결과가 아닙니다. 입력 형식을 포함한 실제 token 측정은 별도입니다.
    # BEGIN D21-04-A02

    # 가상 토큰 예산 파라미터 정의
    parts = {"window":8192,"instructions_question":800,"examples":600,"output_reserve":1600,"margin":256}
    # 전체 윈도우 크기에서 각 요소를 차감하여 가용 공간 계산
    available = parts["window"]-parts["instructions_question"]-parts["examples"]-parts["output_reserve"]-parts["margin"]  # TODO: window에서 지시·질문, 예제, 출력 예약, 여유를 뺍니다.
    # 예산 계산 결과 딕셔너리 생성
    result = {"source":"hypothetical_budget_not_model_measurement", "parts":parts, "available_for_context":available}
    # 가용 공간이 4936인지 단언 검증
    assert available == 4936
    # TODO: 결과 4936과 비교. len(text)를 token 수라고 부르지 마세요.
    # raise NotImplementedError("D21-04-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A02
    return result

# 메인 실행 함수
# - 데이터 로드, 컨텍스트 선택, 예산 산출, 파일 저장 및 검증 수행
def main() -> None:
    # 전체 지식 데이터 로드
    rows=read_json(DATA/"knowledge_v1.json")
    # ID 102 선택을 통한 컨텍스트 및 JSON 직렬화 수행
    chosen, context_json=select_context(rows,[102])
    # 가상 토큰 예산 계산 수행
    budget=calculate_budget()
    # TODO D21-04-A03: 포함·제외 ID와 원문·예산을 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 포함 [102], 제외 101·103. 실제 입력 원문을 보존합니다.
    # BEGIN D21-04-A03

    # 포함된 지식 ID 목록 추출
    included_ids = []  # TODO: chosen의 id 목록
    # 제외된 지식 목록 초기화
    excluded = []
    for row in rows:
        # 포함되지 않은 항목에 대해 제외 이유 기록
        if row["id"] not in included_ids:
            excluded.append({"id":row["id"], "reason":"이번 서버 실행 질문에서 선택하지 않음"})  # TODO: 제외 이유
    # 매니페스트 정보 정의
    manifest = {"context_version":"knowledge_v1", "included_ids":included_ids, "excluded":excluded, "budget":budget}
    # 컨텍스트 JSON 및 매니페스트 파일 저장
    write_text(HERE/"outputs"/"context.json", context_json)  # TODO: context_json
    write_json(HERE/"outputs"/"context_manifest.json", manifest)
    # raise NotImplementedError("D21-04-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A03
    # TODO D21-04-A04: 중복 선택은 제거하고, 스냅샷 중복 ID와 없는 ID는 오류인지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 중복 선택과 잘못된 원본 ID를 구분합니다.
    # BEGIN D21-04-A04

    # 중복 포함 선택 테스트
    dedup, _ = select_context(rows, [102,102,101])
    # 중복 제거 및 순서 보존 여부 검증
    assert [r["id"] for r in dedup]==[102,101]
    # 오류 감지 목록 초기화
    errors = []
    # TODO: [102,101]인지 확인하고 [999]·스냅샷 중복을 각각 try/except ValueError로 검사
    # 실패를 무시한 채 조용히 지식을 누락시키지 마세요.

    # 잘못된 ID 및 중복 스냅샷에 대한 예외 발생 여부 검사
    for records,ids in [(rows,[999]),(rows+[rows[0]],[101])]:
        try:
            select_context(records,ids)
        except ValueError:
            errors.append(True)
        else:
            errors.append(False)
    # 모든 오류 감지가 정상 발생했는지 단언 검증
    assert all(errors)
    # 선택 검증 결과 파일 저장
    write_json(HERE/"outputs"/"selection_checks.json",{"dedup_ids":[r["id"] for r in dedup],"errors_detected":errors})
    # raise NotImplementedError("D21-04-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A04
    # TODO D21-04-A05: 허용·유효성·관련성 검토를 선택 이유와 함께 적으세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 기록만으로 권한 통제가 구현된 것은 아닙니다. 자료 선정 정책을 설명하는 활동입니다.
    # BEGIN D21-04-A05

    # 컨텍스트 정책 정의
    policy = {"permissions":"수업용 가상 지식만 사용","validity":"knowledge_v1 고정","relevance":"서버 실행 위치는 102",
              "order":"요청한 selected_ids의 첫 순서","excluded_when_over_budget":"중복·무관 정보부터 검토, 실제 tokenizer로 재측정 필요"}
        # TODO: 가상 자료의 허용·유효성·관련성·순서 정책 작성 후 저장

    # 컨텍스트 정책 파일 저장
    write_json(HERE/"outputs"/"context_policy.json",policy)
    # raise NotImplementedError("D21-04-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A05
    # TODO D21-04-A06: 원문과 canonical JSON 해시를 함께 보존하고 순서 차이를 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 키 정렬은 목록 순서를 바꾸지 않습니다. 해시는 값의 진실성·권한을 보증하지 않습니다.
    # BEGIN D21-04-A06

    # 정규화된 텍스트 및 해시 생성
    canonical_text = canonical(chosen)
    context_hash = sha_text(canonical_text)  # TODO: UTF-8 SHA-256 제공 함수 사용
    # TODO: 같은 원문은 같은 해시, [101,102]와 [102,101]은 다른 해시인지 확인
    # hash만 남기지 말고 원문도 함께 저장하세요.

    # 동일 내용 재파싱 시 동일 해시 발생 여부 검증
    same_hash=sha_text(canonical(json.loads(canonical_text)))
    assert context_hash==same_hash
    # 순서가 다른 경우 해시 불일치 여부 검증
    forward,_=select_context(rows,[101,102])
    reverse,_=select_context(rows,[102,101])
    assert sha_text(canonical(forward))!=sha_text(canonical(reverse))
    # 해시 및 정규화 텍스트 정보 파일 저장
    write_json(HERE/"outputs"/"context_hash.json",{"canonical_text":canonical_text,"sha256":context_hash,"purpose":"동일 입력 식별; 진실성 보증 아님"})
    # raise NotImplementedError("D21-04-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-A06
    print("[04] Context와 가상 예산 저장 완료. token 실측·검색 결과가 아닙니다.")

"""
본 실습 코드는 지식 저장소에서 특정 ID 목록에 따라 컨텍스트를 선택하고 직렬화하는 로직을 구현하였다.
순서 보존, 중복 제거, 유효성 검증뿐만 아니라 가상 토큰 예산 계산, 매니페스트 작성, 그리고 정규화 기반의 해시 검증을 통해
컨텍스트 관리의 무결성과 재현성을 보장하도록 설계하였다.
"""
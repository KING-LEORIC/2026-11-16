"""Day21 실습 03: 작업 분해와 정보 부족. 실행: python main.py"""
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
# - write_text : 텍스트 파일 쓰기 함수
from coursekit.io import DATA, read_json, write_json, write_text

# 기준: Day21 PPT 21~27장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

"""지식 카드 정보를 분석하여 요구 사실과 지원 사실을 대조하고 정보 부족 상태를 판정하는 함수"""

# 카드 분석 함수
# - card : 분석할 카드 딕셔너리 데이터
def analyze_card(card):
    # TODO D21-03-A01: 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요.
    # 입력·대상: 교사가 작성한 required/supported/conflicts 카드
    # 완료 기준: C01 missing=[], C02 missing=[보관 기간]
    # 핵심: 이 코드는 자유로운 질문의 의미를 자동 이해하지 않습니다. 명시된 판단 카드를 처리합니다.
    # BEGIN D21-03-A01

    # 필수 요구 사실 목록 추출
    required = list(card["required"])   # TODO: card["required"]
    # 지원되는 사실 목록 추출
    supported = card["supported"]   # TODO: card["supported"]
    # 누락된 사실 목록 초기화
    missing = []
    for fact in required:
        # 지원되지 않는 사실인 경우 누락 목록에 추가
        if fact not in supported:    # TODO: supported에 없는 fact인지
            missing.append(fact)
    # 상충하는 사실 목록 추출
    conflicts = list(card["conflicts"])   # TODO: card["conflicts"]
    # raise NotImplementedError("D21-03-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-A01
    # TODO D21-03-A02: 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 오늘 계약은 부분 답변을 새 상태로 추가하지 않습니다. 충분한 근거가 없으면 명시적으로 멈춥니다.
    # BEGIN D21-03-A02

    # 누락 또는 상충 정보가 있으면 정보 부족, 없으면 답변 완료 상태 설정
    status = "insufficient_context" if missing or conflicts else "answered"  # TODO: missing 또는 conflicts가 있으면 부족, 아니면 answered
    # 출처 식별자 목록 초기화
    source_ids = []
    if status == "answered":
        for fact in required:
            # 지원 사실의 출처 식별자 추가
            source_ids.extend([supported[fact]])  # TODO: supported[fact]
    # 중복 출처 식별자 제거
    source_ids=list(dict.fromkeys(source_ids))
    # 분석 결과 딕셔너리 생성
    result = {"case_id":card["case_id"],"required":required,"supported_facts":list(supported),
              "missing":missing,"conflicts":conflicts,"status":status,"source_ids":source_ids,
              "basis":"teacher_authored_fact_card"}
    # raise NotImplementedError("D21-03-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-A02
    return result

# 메인 실행 함수
# - 카드 데이터 로드, 분석 결과 저장 및 검증 수행
def main():
    # 판단 카드 데이터 로드
    cards=read_json(DATA/"decomposition_cards.json")
    # TODO D21-03-A03: 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 2개 결과와 작업 지시를 저장합니다. 모델 추론 관찰 기록이 아닙니다.
    # BEGIN D21-03-A03

    results = []
    for card in cards[:2]:
        # 상위 카드 2개에 대한 분석 결과 추가
        results.append(analyze_card(card))  # TODO: analyze_card(card)
    # 모델 작업 지시사항 정의
    instruction = "질문이 요구하는 사실과 근거를 대조하세요. 부족하면 추측하지 말고 필요한 정보를 적으세요. 내부 사고 기록 대신 최종 JSON만 반환하세요."  # TODO: 사실 대조·부족 처리·최종 JSON 요구(긴 내부 사고 요구 X)
    # 분석 결과 및 작업 지시사항 파일 저장
    write_json(HERE/"outputs"/"task_cards.json", results)
    write_text(HERE/"outputs"/"task_instruction.txt", instruction)
    # raise NotImplementedError("D21-03-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-A03
    # TODO D21-03-A04: 위치와 기간을 함께 묻는 질문에서 빠진 사실을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 없는 보관 기간을 위치 정보로 추측하지 않습니다.
    # BEGIN D21-03-A04

    # 복합 질문 카드 분석
    compound = analyze_card(cards[2])
    # TODO: 위치는 있지만 기간은 없음. 부분 answered로 바꾸지 않는지 검사

    # 누락 항목 및 상태 검증 단언문v
    assert compound["missing"]==["보관 기간"]
    assert compound["status"]=="insufficient_context" and compound["source_ids"]==[]
    # TODO: compound_case.json에 저장

    # 복합 케이스 분석 결과 저장
    write_json(HERE/"outputs"/"compound_case.json",compound)
    # raise NotImplementedError("D21-03-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-A04
    # TODO D21-03-A05: 자료 누락과 상충하는 자료를 다른 이유로 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 날짜가 더 새롭다는 이유만으로 모순이 해결되었다고 자동 판단하지 않습니다.
    # BEGIN D21-03-A05
    
    # 상충 케이스 카드 분석
    conflict = analyze_card(cards[3])
    # 상충 항목 및 상태 검증 단언문
    assert conflict["conflicts"]==["보관 위치"] and conflict["status"]=="insufficient_context"
    # 코드 및 사람 검사 항목 정의
    checks = {"code_checks":["필수 필드","선언한 사실 키","출처 범위"], "human_checks":["질문 해석이 맞는가","각 근거가 실제 주장을 지원하는가","어떤 자료가 유효한가"]}
    # TODO: conflicts와 missing을 구분하고 사람·코드가 검사할 항목을 각각 기록

    # 상충 검토 결과 저장
    write_json(HERE/"outputs"/"conflict_review.json",{"result":conflict,"checks":checks})
    # raise NotImplementedError("D21-03-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-A05
    print("[03] 판단 카드 완료. 근거 대조는 사람의 판단이 포함됩니다.")

"""
본 실습 코드는 질문이 요구하는 사실과 제공된 자료가 지원하는 사실을 비교 분석하여 정보 부족 여부를 판정하도록 구현되어 있다.
작업 카드 분석 로직을 통해 누락된 사실이나 상충되는 조건이 존재할 경우 명시적으로 'insufficient_context' 상태를 부여하고,
복합 질문 및 상충 케이스에 대한 검증을 통해 추측성 답변을 원천 차단하도록 설계하였다.
"""
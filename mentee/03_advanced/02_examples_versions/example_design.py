"""Day21 실습 02: Zero/Few-shot·버전. 실행: python main.py"""
# 파일 경로 조작 기능 사용
# - Path : 경로 객체 생성 및 관리
from pathlib import Path
# 시스템 제어 및 인자 처리 기능 사용
# - sys : 시스템 경로 추가
import sys
# JSON 데이터 직렬화 및 역직렬화 기능 사용
# - json : JSON 변환 처리
import json

# 현재 파일 기준 상위 경로 설정
# - HERE : 현재 파일 디렉터리
# - ROLE_ROOT : 상위 루트 디렉터리
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
# 코스킷 입출력, 프롬프트, 버전 관리 관련 기능 사용
# - DATA : 데이터 경로
# - read_json : JSON 파일 읽기
# - write_json : JSON 파일 쓰기
# - write_text : 텍스트 파일 쓰기
# - save_version : 버전 기록 및 저장
# - make_bundle : 프롬프트 번들 생성
from coursekit.io import DATA, read_json, write_json, write_text, save_version
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 14~20장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.prompting import render_prompt

# 예제 데이터 생성 함수
# - Few-shot 학습을 위한 정상 응답 및 정보 부족 응답 예제 정의
def build_examples():
    # TODO D21-02-A01: 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족 예제 2개. 평가 질문 D/H를 Few-shot에 사용하지 않습니다.
    # 핵심: 입력 예제를 늘려도 모델 가중치가 바뀌는 것은 아닙니다.
    # BEGIN D21-02-A01

    # 예제에 사용할 기준 지식 컨텍스트 정의
    example_context = [{"id":901,"content":"대여 장소는 안내 데스크입니다."}]
    examples = [
        # 정상 응답 예제
        {"question":"어디서 대여하나요?","context":example_context,
            "answer":{"status":"answered","answer":"안내 데스크에서 대여합니다.","source_ids":[901],"missing_information":""}},
        # 정보 부족 응답 예제
        {"question":"대여료는 얼마인가요?","context":example_context,
            "answer":{"status":"insufficient_context","answer":"제공된 지식으로는 답할 수 없습니다.","source_ids":[],"missing_information":"대여료"}},
    ]
    # TODO: 정상 답에는 [901], 정보 부족에는 []와 부족한 사실 이름을 사용합니다.
    # raise NotImplementedError("D21-02-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A01
    return examples

# 메인 실행 함수
# - 예제 생성, 제로샷 및 퓨샷 프롬프트 빌드, 실험 설정, 버전 관리 및 검증 수행
def main():
    examples=build_examples()
    # TODO D21-02-A02: 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt가 생성됩니다. 이는 05의 근거 규칙 A/B와 별도 설계 실험입니다.
    # BEGIN D21-02-A02

    # 평가 케이스 첫 번째 항목 로드
    case = read_json(DATA/"dev_v1.json")[0]
    # 제로샷 번들 생성 (예제 없음)
    zero_bundle = make_bundle(examples=[])     # 예제 없는 입력
    # 퓨샷 번들 생성 (예제 포함)
    few_bundle = make_bundle(examples=examples)      # TODO: examples 사용
    # 제로샷 및 퓨샷 프롬프트 렌더링
    zero_prompt, _ = render_prompt(zero_bundle, case, "A")
    few_prompt, _ = render_prompt(few_bundle, case, "A")
    # TODO: 예제 ID 901의 포함 여부를 확인

    # 제로샷에는 예제 ID가 없고 퓨샷에는 포함되어 있는지 검증
    assert "901" not in zero_prompt and "901" in few_prompt
    # raise NotImplementedError("D21-02-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A02
    # TODO D21-02-A03: 변경점·가설·고정 조건과 두 Prompt를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 가설을 실제 성능 결과처럼 기록하지 않습니다.
    # BEGIN D21-02-A03

    # 실험 메타데이터 정의
    experiment = {
        "experiment":"examples_design_only", "base_version":"examples_zero_v1", "new_version":"examples_few_v1",
        "changed":"예제 유무","hypothesis":"정상과 정보 부족의 출력 조합을 잘 따를지 관찰한다.",
        "fixed":["질문","knowledge_v1","answer_schema_v1","근거 규칙"],"source_mode":"design_only"
    }
    # TODO: 예제 유무를 바꿨다는 기록과 고정 조건을 작성

    # 예제, 실험 정보, 프롬프트 파일 저장
    write_json(HERE/"outputs"/"examples.json", examples)  # TODO: examples
    write_json(HERE/"outputs"/"experiment.json", experiment)
    write_text(HERE/"outputs"/"zero_prompt.txt", zero_prompt)  # TODO: zero_prompt
    write_text(HERE/"outputs"/"few_prompt.txt", few_prompt)   # TODO: few_prompt
    # raise NotImplementedError("D21-02-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A03
    # TODO D21-02-A04: 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기존 examples를 변경하지 않고 새 파일로 저장합니다.
    # BEGIN D21-02-A04

    # 기존 예제 데이터를 깊은 복사하여 새 버전 생성 준비
    replaced = json.loads(json.dumps(examples,ensure_ascii=False))
    replaced[0]["question"]="대여 장소를 알려 주세요."
    # TODO: replaced[0]["question"]만 바꾸고 새 버전·이유 기록
    
    # 수정된 예제 버전 기록 정의
    record={"version":"examples_few_v2","changed":"정상 예제 질문 표현 1개","hypothesis":"의미가 같은 표현에도 출력 계약을 유지하는지 관찰",
            "examples":replaced,"fixed_context":"knowledge_v1","fixed_schema":"answer_schema_v1"}
    # TODO: save_version 사용. 05 A/B에 이 변경을 함께 섞지 마세요.

    # 새 버전 예제 파일 안전 저장
    save_version(HERE/"outputs"/"examples_few_v2.json",record)
    # raise NotImplementedError("D21-02-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A04
    # TODO D21-02-A05: Few-shot 예제에 D/H 질문과 답이 누출되지 않았는지 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 문자열 일치 검사는 최소 보호입니다. 같은 의미로 바꾼 답 누출은 사람이 추가 검토합니다.
    # BEGIN D21-02-A05

    # 개발 및 홀드아웃 평가 케이스 통합 로드
    eval_cases = read_json(DATA/"dev_v1.json") + read_json(DATA/"holdout_v1.json")
    eval_questions = {c["question"] for c in eval_cases}  # TODO: 질문 문자열 집합
    # TODO: 모든 예제의 질문이 평가 질문 집합 밖인지, 예제 출처가 901 범위인지 검사

    # 예제 질문이 평가 데이터와 겹치지 않고 출처 ID가 허용 범위 내인지 검증
    assert all(e["question"] not in eval_questions for e in examples)
    assert all(set(e["answer"]["source_ids"])<= {901} for e in examples)
    # 예제 가드 검증 결과 JSON 저장
    write_json(HERE/"outputs"/"example_guard.json",{"question_overlap":False,"current_context_ids_are_separate":True})
    # raise NotImplementedError("D21-02-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A05
    # TODO D21-02-A06: 동일 버전 덮어쓰기 방지가 실제로 동작하는지 임시 폴더에서 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-02-A06
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as temp:
        path = Path(temp)/"version.json"
        # TODO: 같은 경로에 다른 내용을 저장할 때 ValueError인지 검사

        # 최초 버전 파일 저장
        save_version(path,{"version":"v1","rule":"original"})
        try:
            # 동일 경로에 내용 변경 후 저장 시도 (예외 발생 예상)
            save_version(path,{"version":"v1","rule":"changed"})
        except ValueError:
            blocked=True
        else:
            blocked=False
        assert blocked
    # TODO: 실제 결과를 version_guard.json에 저장

    # 버전 가드 검증 결과 JSON 저장
    write_json(HERE/"outputs"/"version_guard.json",{"overwrite_blocked":blocked})
    # raise NotImplementedError("D21-02-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A06
    print("[02] 예제·버전 설계 완료. 05는 예제 고정, 근거 규칙만 비교합니다.")

"""
본 실습 코드는 Zero-shot 및 Few-shot 프롬프트 설계를 위한 예제 데이터를 구성하고,
동일한 질문에 대해 프롬프트 변동 사항을 체계적으로 실험할 수 있도록 구현되어 있다.
또한, 평가 데이터와의 질문 중복 누출을 방지하는 가드 로직을 적용하고,
`save_version` 함수를 통해 동일 버전 파일의 임의 덮어쓰기를 원천 차단하여
실험 데이터의 무결성과 재현성을 보장하도록 설계하였다.
"""
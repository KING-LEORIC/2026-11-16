"""Day21 실습 08: AI 지식 답변 생성기 v1. 실행: python main.py"""
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
# 코스킷 입출력 및 실험 이름 검증 기능 사용
# - DATA : 데이터 저장 경로
# - read_json : JSON 파일 읽기 함수
# - write_json : JSON 파일 쓰기 함수
# - check_name : 실험 이름 검증 함수
from coursekit.io import DATA, read_json, write_json
# 프롬프트 생성 기능 사용
# - make_bundle : 프롬프트 번들 생성 함수
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 64~72장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
# 실험 준비, 검토, 요약 및 재시도 관련 기능 사용
# - prepare_experiment : 실험 준비 함수
# - review_experiment : 실험 검토 함수
# - summarize : 요약 함수
# - write_summary : 요약 파일 작성 함수
from coursekit.experiments import prepare_experiment, review_experiment, summarize, write_summary
# 픽스처 시나리오 실행 기능 사용
# - run_fixture_scenarios : 픽스처 시나리오 실행 함수
from coursekit.retry import run_fixture_scenarios
from coursekit.io import check_name

"""프롬프트 번들을 선택하고 버전 및 스키마 유효성을 검증하는 함수"""

# 번들 선택 함수
# - bundle_path : 번들 파일 경로 (Path | None)
def choose_bundle(bundle_path=None):
    # TODO D21-08-A01: 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 05 outputs/dev_01/frozen_bundle.json을 선택적으로 지정. 원문을 바꾸지 않습니다.
    # 핵심: 마지막 프로젝트는 기존 흐름을 다시 연결합니다. 새 API·DB·벡터 검색을 만들지 않습니다.
    # BEGIN D21-08-A01

    # 번들 경로 지정 여부에 따른 번들 데이터 로드
    if bundle_path is None:
        bundle = make_bundle()  # 앞 교시 미완성자를 위한 제공 체크포인트
        print("[독립 시작점] 제공 A/B를 사용합니다. D에서 개선한 결과라고 주장하지 않습니다.")
    else:
        bundle=read_json(bundle_path)  # TODO: read_json(bundle_path)
    # TODO: context_version, schema_version, A/B 버전의 존재를 확인

    # 문맥 및 출력 계약 버전 유효성 검사
    if bundle["context_version"]!="knowledge_v1" or bundle["schema_version"]!="answer_schema_v1":
        raise ValueError("수업의 문맥·출력 계약 버전을 확인하세요")
    # 변인 집합이 A와 B로 구성되어 있는지 단언 검증
    assert set(bundle["variants"])=={"A","B"}
    # H 결과를 보고 이 파일을 덮어쓰지 마세요.
    # raise NotImplementedError("D21-08-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A01
    # TODO D21-08-A02: 로드한 출력 계약이 현재 검증 모델과 일치하는지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 계약이 바뀌면 같은 버전으로 비교하지 않습니다.
    # BEGIN D21-08-A02

    from coursekit.contracts import KnowledgeAnswer
    # TODO: bundle["schema"]와 현재 model_json_schema 비교. 불일치면 중단
    # TODO: A/B의 evidence_rule이 서로 다른지 확인

    # 스키마 일치 여부 검사
    if bundle["schema"]!=KnowledgeAnswer.model_json_schema():
        raise ValueError("Prompt와 로컬 검사기의 Schema가 다릅니다")
    # A와 B의 근거 규칙이 서로 다른지 단언 검증
    assert bundle["variants"]["A"]["evidence_rule"]!=bundle["variants"]["B"]["evidence_rule"]
    # raise NotImplementedError("D21-08-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A02
    return bundle

"""홀드아웃 평가 케이스 데이터를 로드하고 필수 선택 ID를 검증하는 함수"""

# 평가 케이스 선택 함수
def choose_cases():
    # TODO D21-08-A03: 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: A/B 각 3질문, 첫 응답 총 6개. H03의 세 근거를 임의로 줄이지 않습니다.
    # BEGIN D21-08-A03

    # 홀드아웃 평가 케이스 로드
    cases = read_json(DATA/"holdout_v1.json")
    # expected_ids = []  # TODO: H01, H02, H03
    # TODO: 세 질문과 선택 ID를 확인. expected_behavior를 Prompt에 넣지 않습니다.

    # 케이스 ID 및 선택된 지식 ID 목록 일치 여부 단언 검증
    assert [c["case_id"] for c in cases]==["H01","H02","H03"]
    assert cases[0]["selected_ids"]==[103]
    assert cases[1]["selected_ids"]==[102]
    assert cases[2]["selected_ids"]==[101,102,103]
    # raise NotImplementedError("D21-08-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A03
    return cases

"""실험 결과 행들을 바탕으로 종합 보고서 딕셔너리를 생성하는 함수"""

# 보고서 생성 함수
# - rows : 실험 결과 행 목록 (list[dict])
def make_report(rows):
    # TODO D21-08-A04: 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족·형식 실패·참조 실패·사람 평가를 구분하고 B의 승리를 강요하지 않습니다.
    # BEGIN D21-08-A04

    # 결과 요약 생성
    report = summarize(rows)
    # 첫 번째 시도 행 필터링
    first = [r for r in rows if r["attempt"]==1]  # TODO: attempt == 1만 선택
    # 프로젝트 요약 정보 정의
    report["project"] = {
        "name":"AI 지식 답변 생성기 v1", "first_target":len(first),
        "not_run":sum(r["execution_state"]=="not_run" for r in first),         # TODO: 미실행 수
        "human_pending":sum(r.get("evidence_ok") is None for r in first),   # TODO: evidence_ok가 None인 수
        "max_attempt":max((r["attempt"] for r in rows),default=0),     # TODO: 최대 attempt
        "completion":"실제 관찰·근거 대조 결과를 확인하세요. 자동 만점/승자 없음",
    }
    # TODO: max_attempt <= 2 확인. 샘플 통과를 모델 우수성으로 적지 마세요.

    # 최대 시도 횟수가 2 이하인지 단언 검증
    assert report["project"]["max_attempt"]<=2
    # raise NotImplementedError("D21-08-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A04
    # TODO D21-08-A05: 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 개선안을 곧바로 같은 H의 독립 검증 성적이라고 주장하지 않습니다.
    # BEGIN D21-08-A05

    # 비교 분석 정보 정의
    report["comparison"]={"first_count":len(first),"retry_count":sum(r["attempt"]==2 for r in rows),
                          "next_improvement":"관찰한 실패를 읽고 지시·예제·문맥 중 하나만 고릅니다.",
                          "holdout_policy":"H를 본 뒤 수정하면 새 버전·새 확인 질문 세트가 필요합니다."}
    # TODO: 실제 개수와 이후 개선 규칙 작성. H 결과를 보고 현재 버전을 고치지 않습니다.
    # raise NotImplementedError("D21-08-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A05
    # TODO D21-08-A06: 출처 유형과 평가 대기 수를 공개하고 실측이 없으면 결론을 보류하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-08-A06

    # 출처 모드 정렬 추출
    modes=sorted({r["source_mode"] for r in rows})
    # 출처 및 평가 관련 정보 정의
    report["provenance"] = {"modes":modes,"manual_runs":sum(r["source_mode"]=="manual_chat" and r["execution_state"]!="not_run" for r in first),
                            "fixture_rows":sum(r["source_mode"]=="fixture" for r in rows),
                            "decision":"사람이 질문·주장·출처를 대조한 뒤 판단. 프로그램은 우열을 결정하지 않습니다."}
    # TODO: 실제 데이터의 출처와 실행 수 계산. 없는 실험을 채워 넣지 않습니다.
    # raise NotImplementedError("D21-08-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A06
    return report

"""반복 관찰 횟수를 설정하고 반환하는 함수"""

# 반복 횟수 선택 함수
def choose_repeats():
    # TODO D21-08-A07: 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기본 6개와 반복 6개를 별도 슬롯으로 기록합니다.
    # BEGIN D21-08-A07

    # 반복 관찰 횟수 정의
    repeats = 2  # TODO: 총 2회. 실제로 못한 항목은 not_run으로 보존
    # raise NotImplementedError("D21-08-A07: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-A07
    return repeats

"""명령행 인자에 따라 실험 준비, 검토 또는 픽스처 샘플 검사를 수행하는 메인 함수"""

# 메인 실행 함수
# - 명령행 파서 구성 및 실행 제어 수행
def main():
    import argparse
    # 인자 파서 생성
    parser=argparse.ArgumentParser(description="모델 호출 없이 Prompt 준비 또는 실제 수동 응답 검토")
    parser.add_argument("command",choices=["prepare","review","fixtures"],nargs="?",default="prepare")
    parser.add_argument("--run",default="holdout_01",help="영문 실험 폴더명; 기존 실험 덮어쓰기 금지")
    parser.add_argument("--bundle",type=Path,help="05에서 고정한 frozen_bundle.json. 미지정 시 제공 독립 시작점 사용")
    # 인자 파싱 수행
    args=parser.parse_args()
    # 실험 이름 유효성 검사
    check_name(args.run)
    folder=HERE/"outputs"/args.run
    # 명령어별 분기 처리
    if args.command=="prepare":
        # 실험 준비 단계 실행
        bundle=choose_bundle(args.bundle)
        cases=choose_cases()
        repeats=choose_repeats()
        prepare_experiment(folder,bundle,cases,repeats=repeats)
        print("[준비]",folder)
        print("prompts의 원문을 각각 새 대화에 입력하세요. 아직 실제 응답은 0개입니다.")
    elif args.command=="review":
        # 실험 검토 단계 실행
        rows=review_experiment(folder)
        report=make_report(rows)
        write_summary(folder,report)
        print("[검토]",folder/"summary.md")
        print("raw가 없는 항목은 미실행, 사람 평가 null은 미평가입니다.")
    else:
        # 픽스처 샘플 검사 실행
        results=run_fixture_scenarios(read_json(DATA/"validation_fixtures.json"))
        write_json(HERE/"outputs"/"fixture_checks.json",{"source_mode":"fixture","results":results})
        print("[샘플 검사] 호출 수 2·2·1·1. 모델의 실제 복구율이 아닙니다.")

"""
본 실습 코드는 AI 지식 답변 생성기 v1 프로젝트의 최종 통합 실행 스크립트로,
A/B 실험 번들 로드, 홀드아웃 평가 케이스 설정, 실험 준비 및 검토 결과 요약 보고서 생성을 지원하도록 구현하였다.
"""
# Perplexity Advanced MCP

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/code-yeongyu/perplexity-advanced-mcp)
[![PyPI](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/perplexity-advanced-mcp)

</div>

---

## 개요

Perplexity Advanced MCP는 [OpenRouter](https://openrouter.ai/)와 [Perplexity](https://docs.perplexity.ai/home) API를 활용하여 향상된 쿼리 처리 기능을 제공하는 고급 통합 패키지입니다. 직관적인 명령줄 인터페이스와 강력한 API 클라이언트를 통해 단순 및 복잡한 쿼리 모두에 대해 AI 모델과의 원활한 상호작용을 지원합니다.

## [perplexity-mcp](https://github.com/jsonallen/perplexity-mcp)와의 비교

[perplexity-mcp](https://github.com/jsonallen/perplexity-mcp)가 [Perplexity](https://docs.perplexity.ai/home) AI의 API를 사용한 기본적인 웹 검색 기능을 제공하는 반면, Perplexity Advanced MCP는 다음과 같은 추가 기능을 제공합니다:

- **다중 공급자 지원:** [Perplexity](https://docs.perplexity.ai/home)와 [OpenRouter](https://openrouter.ai/) API를 모두 지원하여 공급자 선택의 유연성 제공
- **쿼리 타입 최적화:** 단순 쿼리와 복잡한 쿼리를 구분하여 비용과 성능을 최적화
- **파일 첨부 지원:** 쿼리에 파일 내용을 컨텍스트로 포함하여 더 정확하고 맥락에 맞는 응답 제공
- **향상된 재시도 로직:** 안정성 향상을 위한 강력한 재시도 메커니즘 구현

전반적으로, 이는 [Cline](https://cline.bot/)이나 [Cursor](https://www.cursor.com/)와 같은 에디터와 통합할 때 코드베이스를 다루는 데 가장 적합한 MCP입니다.

## 기능

- **통합 API 클라이언트:** 단순 및 복잡한 쿼리 처리를 위한 구성 가능한 모델과 함께 [OpenRouter](https://openrouter.ai/)와 [Perplexity](https://docs.perplexity.ai/home) API 지원
- **명령줄 인터페이스 (CLI):** [Typer](https://typer.tiangolo.com/)를 사용한 API 키 구성 및 MCP 서버 실행 관리
- **고급 쿼리 처리:** 쿼리에 컨텍스트 데이터를 포함할 수 있는 파일 첨부 처리 기능 통합
- **강력한 재시도 메커니즘:** 일관되고 안정적인 API 통신을 위한 Tenacity 기반 재시도 로직
- **사용자 정의 가능한 로깅:** 상세한 디버깅 및 런타임 모니터링을 위한 유연한 로깅 구성

## 최적의 AI 구성

AI 어시스턴트([Cursor](https://www.cursor.com/), [Claude for Desktop](https://claude.ai/download) 등)와의 최상의 경험을 위해 프로젝트 지침이나 AI 규칙에 다음 구성을 추가하는 것을 권장합니다:

```xml
<perplexity-advanced-mcp>
    <description>
        Perplexity는 인터넷을 검색하고, 정보를 수집하며, 사용자의 질문에 답변할 수 있는 LLM입니다.

        예를 들어, Python의 최신 버전을 알아내고 싶다고 가정해 봅시다.
        1. Google에서 검색합니다.
        2. 상위 2-3개의 결과를 직접 읽고 확인합니다.

        Perplexity가 이 작업을 대신 수행합니다.

        사용자의 질문에 답하기 위해 Perplexity는 검색을 수행하고, 상위 검색 결과를 열어 해당 웹사이트에서 정보를 찾은 다음 답변을 제공합니다.

        Perplexity는 단순 및 복잡한 두 가지 유형의 쿼리에 사용할 수 있습니다. 사용자의 요청을 충족시키기 위해 적절한 쿼리 유형을 선택하는 것이 가장 중요합니다.
    </description>
    <simple-query>
        <description>
            저렴하고 빠릅니다. 하지만 복잡한 쿼리에는 적합하지 않습니다. 평균적으로 복잡한 쿼리보다 10배 이상 저렴하고 3배 더 빠릅니다.
            "Python의 최신 버전은 무엇인가요?"와 같은 간단한 질문에 사용합니다.
        </description>
        <pricing>
            입력 토큰당 $1/M
            출력 토큰당 $1/M
        </pricing>
    </simple-query>

    <complex-query>
        <description>
            더 느리고 비쌉니다. 단순 쿼리와 비교하여 평균적으로 10배 이상 비싸고 3배 더 느립니다.
            "첨부된 코드를 분석하여 특정 라이브러리의 현재 상태를 검토하고 마이그레이션 계획을 수립하세요"와 같이 여러 단계의 추론이나 심층 분석이 필요한 요청에 사용합니다.
        </description>
        <pricing>
            입력 토큰당 $1/M
            출력 토큰당 $5/M
        </pricing>
    </complex-query>

    <instruction>
        사용자의 요청을 검토할 때 예상치 못하거나, 불확실하거나, 의문스러운 점이 있다면, **그리고 인터넷에서 답을 얻을 수 있다고 생각된다면** "ask_perplexity" 도구를 사용하여 Perplexity에 문의하는 것을 주저하지 마세요. 하지만 인터넷이 사용자의 요청을 만족시키는 데 필요하지 않다면, perplexity에 문의하는 것은 의미가 없습니다.
        Perplexity도 LLM이므로 프롬프트 엔지니어링 기법이 매우 중요합니다.
        명확한 지침 제공, 충분한 컨텍스트, 예시 제공 등 프롬프트 엔지니어링의 기본을 기억하세요.
        사용자의 요청을 원활하게 충족시키기 위해 가능한 한 많은 컨텍스트와 관련 파일을 포함하세요. 파일을 첨부할 때는 반드시 절대 경로를 사용해야 합니다.
    </instruction>
</perplexity-advanced-mcp>
```

이 구성은 AI 어시스턴트가 Perplexity 검색 기능을 언제 어떻게 사용할지 더 잘 이해하도록 도와주며, 비용과 성능 모두를 최적화합니다.

## 사용법

### [uvx](https://docs.astral.sh/uv/guides/tools/)를 사용한 빠른 시작

MCP 서버를 실행하는 가장 쉬운 방법은 [uvx](https://docs.astral.sh/uv/guides/tools/)를 사용하는 것입니다:

```sh
uvx perplexity-advanced-mcp -o <openrouter_api_key> # 또는 -p <perplexity_api_key>
```

환경 변수를 사용하여 API 키를 구성할 수도 있습니다:

```sh
export OPENROUTER_API_KEY="your_key_here"
# 또는
export PERPLEXITY_API_KEY="your_key_here"

uvx perplexity-advanced-mcp
```

참고:
- OpenRouter와 Perplexity API 키를 동시에 제공하면 오류가 발생합니다
- CLI 인수와 환경 변수가 모두 제공된 경우 CLI 인수가 우선합니다

CLI는 [Typer](https://typer.tiangolo.com/)로 구축되어 사용자 친화적인 명령줄 경험을 제공합니다.

### MCP 검색 도구

이 패키지는 `ask_perplexity` 함수를 통해 통합된 MCP 검색 도구를 포함합니다. 단순 및 복잡한 쿼리를 모두 지원하며 추가 컨텍스트를 제공하기 위한 파일 첨부를 처리합니다.

- **단순 쿼리:** 빠르고 효율적인 응답 제공
- **복잡한 쿼리:** 상세한 추론을 수행하고 XML 형식의 파일 첨부를 지원

## 구성

- **API 키:** 명령줄 옵션이나 환경 변수를 통해 `OPENROUTER_API_KEY` 또는 `PERPLEXITY_API_KEY` 구성
- **모델 선택:** 구성(`src/perplexity_advanced_mcp/config.py`)에서 쿼리 유형을 특정 모델에 매핑:
  - **[OpenRouter](https://openrouter.ai/):**
    - 단순 쿼리: `perplexity/sonar`
    - 복잡한 쿼리: `perplexity/sonar-reasoning`
  - **[Perplexity](https://docs.perplexity.ai/home):**
    - 단순 쿼리: `sonar-pro`
    - 복잡한 쿼리: `sonar-reasoning-pro`

## 개발 배경 및 철학

이 프로젝트는 개인적인 호기심과 실험에서 시작되었습니다. 최근의 ["vibe coding"](https://x.com/karpathy/status/1886192184808149383) 트렌드를 따라, 코드의 95% 이상이 [Cline](https://cline.bot/) + [Cursor](https://www.cursor.com/) IDE를 통해 작성되었습니다. "말은 쉽고 코드를 보여달라"고들 하죠 - [Wispr Flow](https://wisprflow.ai/)의 음성-텍스트 변환 마법 덕분에, 저는 말 그대로 이야기를 했고 코드가 나타났습니다! 대부분의 개발은 "x y z에 대한 코드를 작성해줘, x y z의 버그를 수정해줘"라고 말하고 엔터를 누르는 것으로 이루어졌습니다. 놀랍게도 이 완전히 기능하는 프로젝트를 만드는 데 몇 시간도 걸리지 않았습니다.

프로젝트 스캐폴딩부터 파일 구조까지, 모든 것이 LLM을 통해 작성되고 검토되었습니다. GitHub Actions 워크플로우를 통한 PyPI 배포와 릴리즈 승인 과정까지도 Cursor를 통해 처리되었습니다. 인간 개발자로서 제 역할은 다음과 같았습니다:

- AI가 적절한 테스트를 수행할 수 있도록 MCP 서버 시작 및 중지
- 오류 발생 시 로그 복사 및 제공
- 인터넷에서 [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) 문서와 예제 찾아서 제공
- 올바르지 않아 보이는 코드에 대한 수정 요청
- AI가 전체 CI/CD 파이프라인을 설정한 후 최종 릴리즈 승인

많은 것들이 자동화되고 대체될 수 있는 오늘날의 세상에서, 이 MCP가 여러분과 같은 개발자들이 단순히 코드를 작성하는 것을 넘어서는 가치를 발견하는 데 도움이 되기를 바랍니다. 이 도구가 여러분이 더 높은 수준의 결정과 고려사항을 다루는 새로운 시대의 개발자가 되는 데 도움이 되기를 바랍니다.

## 개발

이 패키지에 기여하거나 수정하려면:

### 1. **저장소 복제:**

```sh
gh repo clone code-yeongyu/perplexity-advanced-mcp
```

### 2. **의존성 설치:**

```sh
uv sync
```

### 3. **기여:**

기여는 환영합니다! 기존 코드 스타일과 커밋 가이드라인을 따라주세요.

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

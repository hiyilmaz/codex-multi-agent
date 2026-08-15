# Graphify Trigger Problem Investigation Packet

Date: 2026-08-10
Scope: Read-only forensic reconstruction of EXP-20260810-003 through EXP-20260810-007

# 1. Executive factual summary

Bu incelemenin ana bulguları:

1. Mevcut aktif yapı bir “repository reader runtime” değil, policy-only bir yönlendirme katmanıdır. Repository, aktif ARK adapter/wrapper/sandbox bulunmadığını açıkça belirtiyor; router yalnızca aday aracı seçiyor ve execution yetkisi vermiyor. [CMA_ARK_PLANNING_PROPOSAL.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/docs/CMA_ARK_PLANNING_PROPOSAL.md:1), [CMA_REPO_TOOLS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/registry/modules/CMA_REPO_TOOLS.md:27)

2. `bounded-reader`, kalıcı production kodunda veya testlerde tanımlanmış ortak bir abstraction değildir. Bağlayıcı anlamı EXP-005–007 için oluşturulan, daha sonra silinen geçici JSONL validator’larından gelir.

3. EXP-007’de shell kullanımı tek başına yasak değildi. Geçen exact, filename ve known-file probları da `/bin/zsh -lc` üzerinden çalıştı. Generic probu düşüren birleşim şuydu:

   - ilk komutun başarısız exit üretmesi,
   - `&&` ve `;` ile shell composition,
   - allowlist dışı `ls` ve `wc`,
   - modelin bir yerine iki fallback komutu üretmesi.

4. EXP-007 oracle’ında “bounded” şu öğelerin birleşimiydi:

   - en fazla 1–2 top-level `command_execution`,
   - yalnızca `rg` veya `sed`,
   - compound shell operatörü olmaması,
   - belirtilen fixture dosyasının relative operand olarak bulunması,
   - absolute path ve basit `..` biçimlerinin olmaması,
   - başarılı exit,
   - exact final output,
   - Graphify/module aktivitesi olmaması.

   Buna karşılık byte/line limiti, symlink çözümü ve tam path containment, çalışan validator tarafından eksiksiz enforce edilmedi.

5. Generic-content için `sed`, `ls` ve `wc` kullanılması repository’de deterministik bir code path tarafından zorunlu kılınmıyor. Bunlar raw trace’te model tarafından üretilmiş shell komutlarıdır. Runtime planner/dispatcher kaynak kodu bu repository’de olmadığı için modelin iç seçim algoritması code-level olarak incelenemiyor.

6. Repository okumasına yol açabilecek bütün OS-level komutların geçtiği repository-owned tek bir choke point yoktur. Codex’in top-level command tool çağrıları JSONL’de görünür; ancak shell child’ları, Python/Node içindeki doğrudan file-open çağrıları ve runtime’ın kendi policy/context okumaları ayrı ayrı görünmez.

7. Kalıcı testler yalnızca Markdown policy/module sözleşmesini denetler. Canlı task komutu, executable allowlist’i, path containment veya file-open auditing yapan kalıcı bir test bulunmuyor. [test_cma_lazy_runtime.py](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/tests/test_cma_lazy_runtime.py:25)

8. Güncel doğrulamada:

   - deneysel `.exp00*` ve `/tmp/cma-graphify-*` kökleri bulunmadı,
   - policy template, portable policy ve aktif policy aynı hash’te,
   - aktif Graphify/module/config deney öncesi hash’lerde,
   - config `0600`,
   - yalnızca [governance/EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:1) çalışma ağacında değişmiş durumda.

Testler bu investigation sırasında yeniden çalıştırılmadı; rollback sonrası `26/26` ve `157/157` sonuçları deney kayıtlarından doğrulandı. [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:246)

# 2. Acceptance criteria matrix

| Kriter | Kaynak | Teknik PASS | Teknik FAIL |
|---|---|---|---|
| Exact search | EXP-007 success criteria ve disposable validator; [record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:40), [trace validator](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1507) | Exact normalized output; en az bir başarılı task command; her inner executable `rg`; needle argv’de; compound operator yok; Graphify/module yok | Yanlış/eksik output; non-`rg`; `&&`, `;`, pipe, redirection vb.; module/Graphify aktivitesi; failed command |
| Filename search | Aynı record; [trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1522) | Final `named_fixture.cfg`; executable `rg`; `--files`; exact filename operative glob/pattern içinde; composition ve Graphify yok | Filename yalnızca output veya incidental arg olarak geçiyorsa; non-`rg`; module/Graphify; compound shell |
| Known-file read | [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:45), [validator/trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1537) | Exact one-line value; 1–2 successful events; executable `rg` veya `sed`; operand `named_fixture.cfg`; absolute/`..` yok; composition ve Graphify yok | Başka executable; broad/root read; absolute/`..`; composition; failed event; yanlış final; Graphify/module |
| Generic-content | Aynı acceptance; [failed trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1556) | Exact `EXP007_PROJECT_PURPOSE`; 1–2 başarılı events; yalnızca `rg`/`sed`; `README.md` operandı; no composition; no Graphify | İlk unsuccessful command; `&&`/`;`; `ls`/`wc`; yanlış output/path; module/Graphify |
| `bounded-reader` | EXP-005–007 experiment-local oracle; [EXP-007](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:43) | Yukarıdaki executable, count, operand, exit, output ve no-composition koşullarının birleşimi | Bunlardan herhangi birinin ihlali |
| Production router contract | [CMA_REPO_TOOLS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/registry/modules/CMA_REPO_TOOLS.md:14), [tests](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/tests/test_cma_lazy_runtime.py:242) | Exact text/path için `rg`; architecture için Graphify; narrowest sufficient tool; yeterli kanıtta dur | Static policy satırlarının veya authority boundary’nin eksik olması |
| Live process restriction | Kalıcı tanım yok | Undefined | Undefined |

`bounded-reader` sorularının kesin karşılığı:

| Soru | Kanıta dayalı cevap |
|---|---|
| Yasak belirli binary’ler mi? | Evet. Known/generic için allowlist `{rg, sed}` idi. |
| Shell kullanımı mı yasak? | Hayır. Geçen bütün problarda `/bin/zsh -lc` vardı. |
| Compound command yasak mı? | Evet. `&&`, `||`, `;`, `|`, redirection, `$(` ve newline reddediliyordu. |
| İzinli primitive kümesinin dışına çıkmak yasak mı? | Evet. `ls` ve `wc` bu nedenle ihlaldi. |
| Dosya okuma miktarı sınırlandı mı? | Acceptance metni “bounded” diyor; çalışan EXP-007 validator sed range veya byte miktarını tam parse etmiyordu. Bu boyut kısmen tanımlı, eksik enforce edilmişti. |
| Subprocess sayısı sınırlandı mı? | Known/generic için 1–2 top-level `command_execution`. Exact/filename’de bu count aynı açıklıkta sabitlenmedi. |
| Modelin seçtiği bütün helper’lar kapsamda mı? | JSONL’ye `command_execution` olarak düşenler evet. Internal FS API ve child process’ler ayrı görünmediği için bütün gerçek helper’ların kapsandığı kanıtlanamaz. |
| Symlink/path containment enforce edildi mi? | TDD tasarım metninde istenmişti; çalışan inline validator yalnızca string tabanlı absolute/`..` kontrolü yaptı. Tam `realpath`/symlink enforcement kanıtlanmadı. |

# 3. EXP-003–EXP-007 forensic reconstruction

## EXP-003 — Repository Router Usage Measurement

Kaynak: [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:318)

**Amaç:** Exact-text lookup’ın yalnızca `rg`, basit control task’ın sıfır tool kullanıp kullanmadığını ve token/zaman maliyetini gözlemlemek.

**Değişiklik:** Production/policy değişikliği yok. İki ephemeral read-only probe planlandı.

**Probe:** Kayıt “one fixed exact-text lookup” diyor; temizlenen private harness nedeniyle exact prompt literal’i artık authoritative repository kaydında bulunmuyor.

**Beklenen:**

- iki original run,
- her birinde bir geçerli usage event,
- routed run’da yalnızca narrowest approved command,
- control’da sıfır tool,
- doğru output ve state parity.

**Gerçek:**

1. Graphify duyurusu,
2. Graphify skill’in 699 satırının dört shell command ile okunması,
3. `rg` pipeline,
4. doğru exact path,
5. iki agent message,
6. control hiç çalıştırılmadı.

Usage: `163,172` input, bunun `132,864`ü cached; `839` output ve `294` reasoning output token. [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:356)

**Reject:** “Only narrowest approved local command” ve minimal-command kriterleri ihlal edildi.

**Kesin çıkarım:** O fresh session ve o prompt için doğru cevap, gereksiz Graphify skill okumalarıyla birlikte geldi.

**Çıkarılamaz:**

- Graphify’ın her exact search’te yükleneceği,
- token farkının tamamının Graphify’dan kaynaklandığı,
- control ile karşılaştırmalı latency/cost,
- belirli bir dispatcher bug’ı,
- model dışındaki runtime component’inin yanlış seçim yaptığı.

## EXP-004 — Narrow Graphify Skill Activation

Kaynak: [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:254)

**Amaç:** Yalnız Graphify frontmatter description’ını daraltarak dört basit repository-content task’ında Graphify’ı devre dışı bırakmak.

**Değişiklik:** Aktif `~/.codex/skills/graphify/SKILL.md` frontmatter description; skill body/router/config korunacaktı.

**Exact probe:**

```text
Use the narrowest sufficient local tool. Find the exact text
ROUTER_SENTINEL_20260810 and return exactly the relative path,
line number, and matching line in rg format. Do not modify files.
```

**Diğer problar:**

- filename: `named_fixture.cfg`,
- known-file: aynı dosyanın one-line value’su,
- generic: README’den project purpose,
- `/graphify --help`,
- cross-file `source.py` → `target.py`.

**Baseline araç sırası:**

1. `sed -n 1,240p Graphify/SKILL.md`
2. aynı compound command içinde `sed -n 1,240p CMA_REPO_TOOLS.md`
3. sonraki command’da Graphify skill satır `241–520`
4. aynı command’da satır `521–900`
5. `rg -n --fixed-strings ROUTER_SENTINEL_20260810 .`

Raw event: [session line 215](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:215)

**Candidate sonrası:**

- exact doğru fakat module önce `sed` ile okundu,
- filename Graphify’sız geçti,
- generic Graphify’sız fakat `sed` kullandı,
- known-file yalnız `thread.started` + `turn.started` üretti, 91 saniyeyi geçti ve terminate edildi,
- help ve architecture Graphify’ı aktive etti,
- architecture corpus’a geçici trust entry ekledi; sonra temizlendi.

**Reject:** “Dört basit prob yalnızca `rg`” kriteri karşılanmadı; known-file tamamlanmadı.

**Kesin çıkarım:** Dar frontmatter gözlenen basit problarda Graphify false-positive’lerini azalttı; ancak module okumaları ve farklı reader seçimi sürdü.

**Çıkarılamaz:**

- Generic `sed` kullanımının yanlış olduğu; EXP-004’ün oracle’ı bunu yanlış saysa da sonraki deneyler `sed`i izinli hale getirdi.
- Known-file davranışının candidate’dan kaynaklandığı; trace task activity üretmeden stall etti.
- Architecture başarısının yalnız iki code file’a ait olduğu; corpus’ta ek docs vardı ve semantic extraction gözlendi.
- Runtime genelinde Graphify selection’ın deterministik olarak düzeldiği.

## EXP-005 — Graphify Activation Boundary

Kaynak: [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:171)

**Amaç:** Basit lookup’larda Graphify’ı kapatırken known/generic için bounded `rg`/`sed` kullanımını kabul etmek.

**Değişiklik:** Sadece Graphify frontmatter description.

**Probe:**

```text
Find the exact text EXP005_EXACT_SENTINEL and return exactly
the relative path, line number, and matching line in rg format.
Do not modify files.
```

**Baseline trace:**

1. Graphify duyurusu,
2. compound command:
   - `sed Graphify/SKILL.md`
   - `sed CMA_REPO_TOOLS.md`
   - `rg ... ~/.codex/memories/MEMORY.md`
3. `rg --hidden ... -F EXP005_EXACT_SENTINEL`
4. doğru final.

Raw evidence: [session line 866](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:866)

**Candidate sonrası:**

```text
/bin/zsh -lc "
  sed -n '1,240p' ~/.codex/registry/modules/CMA_REPO_TOOLS.md &&
  rg -n --no-heading --color never -F 'EXP005_EXACT_SENTINEL' .
"
```

Final doğru; Graphify skill yüklenmedi. [session line 899](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:899)

**Reject:** Exact lookup için her task executable’ın `rg` olması gerekirken `sed` module read vardı. Completed task activity nedeniyle retry yasaktı.

**Validator bulguları:** Code review, çalıştırılmayan branch’lerde fabricated graph kabulü ve bazı absolute out-of-corpus read’lerin kaçabilmesi riskini buldu. [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:241)

**Kesin çıkarım:** Graphify description değişikliği gözlenen exact probda skill false-positive’ini kaldırdı; router module read’i kaldırmadı.

**Çıkarılamaz:**

- Kalan beş probun sonucu,
- architecture provenance güvenilirliği,
- bütün absolute-path escape’lerin validator tarafından engellendiği,
- `sed`in runtime tarafından zorunlu tutulduğu.

## EXP-006 — Repository Router Trigger Boundary

Kaynak: [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:86)

**Amaç:** Router row ile Graphify metadata’yı birlikte daraltmanın observable farkını göstermek.

**Planlanan değişiklik:** Üç policy kopyasındaki repository-tools router row ve Graphify frontmatter. Production’a hiç yayınlanmadı.

**Baseline probe:**

```text
In this repository, find the exact text "PROJECT_NAME:        Codex Template V2".
Run exactly: rg -n --fixed-strings 'PROJECT_NAME:        Codex Template V2' AGENTS.md.
Return only: AGENTS.md:14:PROJECT_NAME:        Codex Template V2
```

**Beklenen davranışsal RED:** Baseline’ın correct result ile birlikte module/Graphify veya non-prescribed command göstermesi.

**Gerçek:**

```text
/bin/zsh -lc "rg -n --fixed-strings
'PROJECT_NAME:        Codex Template V2' AGENTS.md"
```

Final da exact beklenen değerdi; module/Graphify yoktu. [session line 1314](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1314)

**Reject:** Candidate’ın iyileştirmesini ayırt edecek live RED oluşmadı. Static metadata RED vardı, behavioral RED yoktu.

**Kesin çıkarım:** Bu command-prescriptive input baseline’da zaten geçiyordu.

**Çıkarılamaz:**

- Problemin genel olarak çözülmüş olduğu,
- natural lookup’ın da geçeceği,
- router row değişikliğinin etkisiz olacağı.

## EXP-007 — Direct Local Lookup Fast Path

Kaynak: [EXPERIMENTS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:5)

**Amaç:** Natural lookup için pre-router fast path, advanced-only router row ve positive-only Graphify metadata kombinasyonunu sınamak.

**Değişiklikler:**

- `GLOBAL_AGENTS_TEMPLATE.md`,
- `variants/codex/home/AGENTS.md`,
- aktif `~/.codex/AGENTS.md`,
- Graphify frontmatter,
- geçici focused test kontratı.

Module body ve config değiştirilmedi.

**Fixture:**

```text
alpha.txt            -> EXP007_EXACT_SENTINEL
named_fixture.cfg    -> EXP007_KNOWN_FILE_VALUE
README.md            -> EXP007_PROJECT_PURPOSE
```

**Natural baseline prompt:**

```text
Find the exact text EXP007_EXACT_SENTINEL and return only the
relative path, line number, and matching line. Do not modify files.
```

**Baseline gerçek sıra:**

1. Graphify yönlendirme duyurusu,
2. `sed Graphify/SKILL.md && sed CMA_REPO_TOOLS.md`,
3. `rg --fixed-strings EXP007_EXACT_SENTINEL .`,
4. correct final.

[Raw baseline](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1478)

**GREEN exact:**

```text
rg -n --no-heading --color never [exclusion globs]
'EXP007_EXACT_SENTINEL' .
```

PASS. [Raw exact](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1507)

**GREEN filename:**

```text
rg --files -g 'named_fixture.cfg' -g '!node_modules' -g '!.git'
```

PASS. [Raw filename](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1522)

**GREEN known-file:**

```text
sed -n '1p' named_fixture.cfg
```

PASS. [Raw known-file](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1537)

**Generic gerçek sıra:**

1. Agent message: README’yi salt-okunur kontrol ediyor.
2. `/bin/zsh -lc "rg -n -m 3 \"purpose|Purpose|project|Project\" README.md && sed -n '1,40p' README.md"`
3. `/bin/zsh -lc "ls -l README.md; wc -l README.md; sed -n '1,120p' README.md"`
4. Final: `EXP007_PROJECT_PURPOSE`

[Raw generic trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1556)

**Reject:**

- ilk `rg` araması fixture satırında eşleşme bulmadığından command exit’i başarısızdı,
- `&&` ve `;` kullanıldı,
- `ls` ve `wc` allowlist dışındaydı,
- exact prescribed bounded-reader şekli bozuldu.

**Kesin çıkarım:** Candidate natural exact, filename ve known-file örneklerinde hedef davranışla koreleydi; generic task’ta model additional inspection/fallback komutları üretti.

**Çıkarılamaz:**

- Generic task’ın her zaman aynı komutları üreteceği,
- `ls`/`wc` seçiminin router kodundan kaynaklandığı,
- policy/metadata’nın runtime enforcement sağlayamayacağına dair evrensel ispat,
- başka bir model/runtime sürümünün aynı davranacağı,
- byte/line-bounded reader’ın denenmiş olduğu.

# 4. Execution-path diagrams

Repository’de dispatcher/planner/tool executor implementation’ı yoktur. Aşağıdaki aşamalar yalnız trace ve mevcut policy yüzeyleriyle doğrulanabilen akıştır.

## Ortak aşama sınıflandırması

| Aşama | Gerçek yüzey | Kontrol türü | Runtime enforce edilebilirlik |
|---|---|---|---|
| User/task input | `codex exec` prompt | Deterministik input | Evet, input olarak |
| Dispatcher | Installed `/opt/homebrew/bin/codex` | External runtime | Repository’den belirlenemiyor |
| Policy/context discovery | `AGENTS.md`, global policy/config | Runtime/config-controlled | Runtime tarafından; repo policy advisory |
| Router | Markdown lazy-router row | Configuration-controlled, model-interpreted | Hard enforcement değil |
| Tool metadata | Graphify frontmatter/module text | Configuration-controlled, model-interpreted | Hard enforcement değil |
| Planning/tool selection | Model | Model-controlled | Deterministik değil |
| Tool abstraction | Codex command tool | External runtime | Top-level event görülebilir |
| Process execution | `/bin/zsh -lc <string>` | Wrapper deterministik; inner string model-controlled | Sandbox/process seviyesinde kısmen |
| Filesystem access | `rg`, `sed`, `ls`, `wc` veya interpreter | OS command/API | Seçilen executable’a göre |
| Result | stdout → model → final | Command sonucu + model | Final exact oracle ile doğrulanabilir |

## Exact content search

```text
Natural exact prompt
→ external Codex runtime
→ global/project policy context
→ router/Graphify metadata interpretation
→ model planning
→ command tool
→ /bin/zsh -lc "rg ... needle ."
→ rg opens/searches fixture files
→ stdout match
→ exact final answer
```

EXP-007 baseline’da model planning’den sonra ek branch vardı:

```text
→ sed Graphify skill + sed router module
→ rg
```

## Filename search

```text
Filename prompt
→ external Codex runtime
→ policy/metadata context
→ model chooses rg filename enumeration
→ /bin/zsh -lc "rg --files -g named_fixture.cfg ..."
→ filesystem directory walk by rg
→ relative filename
→ exact final
```

## Known-file read

```text
Known path in prompt
→ external runtime
→ model chooses bounded sed
→ /bin/zsh -lc "sed -n 1p named_fixture.cfg"
→ sed opens exact file
→ one line
→ exact final
```

## Generic-content search

```text
"What is this project about?"
→ external runtime
→ model infers README.md is relevant
→ command 1: rg heuristic terms && sed first 40 lines
→ rg returns no match; compound command fails
→ model emits fallback command
→ command 2: ls ; wc ; sed first 120 lines
→ three utilities inspect/read README metadata/content
→ model returns exact sentinel
```

Router-to-command choice arasında repository’de gösterilebilen deterministic function veya class yoktur.

# 5. Repository-read surface inventory

| Yüzey | Nereden çağrılabilir | Mekanizma | Merkezi wrapper | Audit/engelleme durumu |
|---|---|---|---|---|
| `rg` | Model-generated command; policy’nin preferred exact reader’ı | `/bin/zsh -lc` child process | Repo-owned wrapper yok | Top-level raw command audit edilebilir |
| `grep` | Model shell erişimi; admin scripts | Shell process | Yok | JSONL’de parent string görünür |
| `sed` | Module/skill bootstrap ve file read probları | Shell process | Yok | EXP traces’te görünür |
| `cat` | Model shell; shell installer heredoc/file operations | Shell builtin/executable | Yok | Parent string görünür |
| `head`, `tail` | Model shell; trace inspection | Shell process | Yok | Parent string görünür |
| `awk` | `codex-project-init`, `codex-user-install`, `codex-setup` | Shell-launched argv | Ortak reader wrapper yok | Script source audit edilebilir |
| `find` | Installer tree enumeration | Shell-launched argv | Installer-local validation | General task reader’a bağlı değil |
| `ls`, `wc` | EXP-007 generic model output | Shell process | Yok | Raw command görünür |
| Pipelines/compound | Model command stringleri; shell scripts | zsh parser | Yok | String görünür, child events ayrışmaz |
| Python `open`/`Path.read_*` | `codex-project-upgrade`, record archive, tests; model `python -c` de üretebilir | Direct filesystem API | Component-local | JSONL file-open syscall’ı göstermez |
| `os.open` | `record_archive.py` | Direct API, directory fd + `O_NOFOLLOW` | Sadece records component’i | Güvenli fakat genel değil |
| Node `fs.*` | Production Node source bulunmadı; model shell üzerinden Node çalıştırabilir | Direct API | Yok | Yalnız Node parent command görünür |
| Git | `record_archive.py` ve model-generated git commands | `subprocess.run(argv)` veya shell | General wrapper yok | Git ayrıca object/index/worktree okuyabilir |
| Graphify | Skill body’sinin CLI/Python pipeline’ı | Shell + Python + generated artifacts | Graphify-specific | General reader boundary değil |
| Module loading | Explicit `sed` veya runtime context discovery | Shell ya da internal runtime | Yok | Explicit sed görünür; internal discovery görünmeyebilir |
| Prompt/context assembly | Codex runtime’ın AGENTS/config/skill discovery’si | External runtime internal API | Repository’de yok | JSONL command event garantisi yok |
| Network docs fetch | `scripts/update-openai-codex-docs` `urlopen` | Python network API | Script-local | Repository read problemiyle doğrudan ilgili değil |
| Claude SDK adapter | SDK query, tools tamamen kapalı | Python SDK | Adapter-local denylist | Aktif Codex reader path’i değil |

Direct Python reader örneği: [codex-project-upgrade](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/bin/codex-project-upgrade:97).

Safe component-local reader: [record_archive.py](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/skills/record-archive/scripts/record_archive.py:40).

# 6. Process/shell execution inventory

| Invocation path | Dosya/symbol | Raw string / argv | Shell | Caller | Ortak interception / bypass |
|---|---|---|---|---|---|
| Live Codex task command | External `/opt/homebrew/bin/codex` | Trace’te `/bin/zsh -lc "<model string>"` | Evet | Model/tool runtime | Top-level event görülür; compound/interpreter içi erişim bypass yüzeyi |
| Record archive git check | `is_dirty()`; [source](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/skills/record-archive/scripts/record_archive.py:428) | Tuple argv: `git -C ...` | `shell=False` varsayılanı | Record archive | Güvenilir argv; yalnız bu component |
| Test subprocess’leri | `tests/*.py` | Tuple argv çoğunlukla | Hayır | unittest | Test-only |
| Installer script processes | `bin/*` | Shell script commands | Evet | Explicit admin CLI | Live lookup path’inin parçası değil |
| Claude SDK adapter | `run_query()`; [runner.py](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/adapters/claude-agent-sdk/src/claude_agent_sdk_adapter/runner.py:81) | SDK call, local subprocess değil | N/A | Optional adapter | Live API varsayılan kapalı |
| Graphify CLI/Python | Aktif skill yönergeleri | Çoklu shell/Python command | Evet | Model after skill load | General process guard değil |
| Python/Node one-liner | Model tarafından üretilebilir | Shell → interpreter argv/source | Evet | Model | Parent görünür; interpreter içi open görünmez |
| Git invoked by model | Shell string | Model-controlled | Evet | Model | Record archive wrapper’ını bypass eder |

Tek choke point sorusunun cevabı: **kısmen, fakat güvenilir bir reader choke point olarak hayır.**

- Bütün gözlenen model-generated top-level command’lar Codex command tool’a ve `/bin/zsh -lc` wrapper’ına geldi.
- Fakat repository bu executor’ın source’una sahip değil.
- Shell’in child/grandchild process’leri ayrı event değildir.
- Python/Node doğrudan file open’ları command event olarak ayrışmaz.
- Runtime internal context/module okumaları shell path’inden geçmek zorunda değildir.
- Repository içinde bu yolların tamamını kesen ortak wrapper yoktur.
- OS sandbox bir enforcement boundary olabilir; fakat onun implementation’ı bu repository’de değildir ve `read-only` probları home/config/skill dosyalarının okunmasını engellememiştir.

Installed CLI de `--sandbox` seçeneğini “model-generated shell commands” için tanımlıyor ve `--json` ile JSONL event yayınlıyor. Bu davranış [official non-interactive documentation](https://developers.openai.com/codex/noninteractive) ile uyumludur.

# 7. Generic-content divergence analysis

| Davranış | Kategori | Kanıt |
|---|---|---|
| README.md’nin promptta açıkça belirtilmesi | Deterministik input | Probe literal’i |
| Exact/filename için `rg` route’unun policy’de bulunması | Configuration-controlled | [CMA_REPO_TOOLS.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/registry/modules/CMA_REPO_TOOLS.md:18) |
| `purpose\|Purpose\|project\|Project` pattern’ı | Model-generated | Raw generic trace |
| İlk başarısız search sonrası ikinci command | Model-generated fallback | Raw event sırası |
| `sed -n 1,40p` | Model-generated bounded-ish inspection | Policy bunu zorunlu kılmıyor |
| `ls -l README.md` | Model-generated | Repository’de generic handler kodu yok |
| `wc -l README.md` | Model-generated | Aynı |
| `sed -n 1,120p` | Model-generated broadening | Aynı |
| Agent announcement | Incidental model output | Repository read değil |
| JSONL usage/lifecycle events | Incidental runtime telemetry | `thread/turn/item` events |
| Module/Graphify load | Generic GREEN’de yok | Trace’te skill/module path yok |
| Shell wrapper | External runtime behavior | Bütün geçen problarda da mevcut |

Exact, filename ve known-file task’larında hedef ve primitive biçimi daha belirgindi. Generic task ise “project about” semantiği için model tarafından heuristic arama ve fallback üretti. Bu güçlü bir inference’tır; planner source’u repository’de olmadığı için internal scoring nedeni FACT değildir.

`sed`, `ls`, `wc` sınıfları:

- `sed`: model-generated reader.
- `ls`: model-generated metadata inspection.
- `wc`: model-generated size/line-count inspection.
- Hiçbiri router veya production source tarafından bu generic prompt için deterministik olarak çağrılmıyor.

# 8. Module-loading vs target-repository-read analysis

| Read türü | Experiment oracle’da kapsam | Production spec’te durum |
|---|---|---|
| Target fixture file (`README.md`, `alpha.txt`) | Ana repository-read | Açık |
| `CMA_REPO_TOOLS.md` explicit `sed` | Negative/simple probe reject nedeni | Router load olarak tanımlı; bounded-reader ile ilişkisi tanımsız |
| Graphify `SKILL.md` explicit `sed` | Reject/activation evidence | Skill load olarak tanımlı |
| Aktif/global policy okunması | Trace’te explicit command ise görünür | Runtime context load kapsamı tanımsız |
| Runtime implementation source | Problarda yok | Undefined |
| AGENTS/config internal discovery | JSONL’de file-read event değil | Undefined |
| Memory dosyası | EXP-005 baseline’da explicit out-of-corpus read | Negative probe açısından unwanted |
| Graphify-generated artifacts | Architecture positive probe’da istenen; simple probe’da forbidden | Task türüne bağlı |

Sonuç:

- Experiment acceptance, explicit module/skill shell okumalarını basit lookup için prohibited task activity saydı.
- Bunun “filesystem read” olduğu tartışmasızdır; `sed` gerçekten dosyayı açtı.
- Ancak target repository okumaları ile system/policy/module okumalarının tek bir production `bounded-reader` kriteri altında aynı şekilde sınıflandırıldığı kalıcı bir spec yoktur.
- Runtime’ın internal context assembly okumalarının aynı kriterde olup olmadığı **undefined/ambiguous**.

# 9. Observability/test blind spots

Mevcut probların gözlem mekanizması:

- `codex exec --ephemeral --json`,
- JSONL lifecycle parsing,
- `item.started` / `item.completed`,
- `command_execution.command`,
- status ve exit code,
- `agent_message`,
- `turn.completed.usage`,
- bazı problarda post-run artifact/path/hash kontrolleri.

Kullanılmayan mekanizmalar:

- syscall/file-open tracing,
- Endpoint Security/audit framework,
- shell history,
- process tree tracing,
- filesystem event stream,
- kernel sandbox log,
- mocked filesystem,
- persistent central command wrapper.

Blind spots:

| Olay | Her zaman görünür mü? | Açıklama |
|---|---|---|
| Top-level Codex command tool invocation | Gözlenen problarda evet | `command_execution` event |
| Top-level successful/failed shell exit | Evet | Shell’in aggregate exit’i |
| Pipeline içindeki her binary | Ayrı event olarak hayır | Yalnız raw shell string içinde görülebilir |
| `&&`/`;` alt komutlarının tek tek exit’i | Hayır | Yalnız shell aggregate exit |
| Shell child/grandchild process | Ayrı event garantisi yok | Parent command text’i parse etmek gerekir |
| Python `open()` / `Path.read_text()` | Hayır | Yalnız Python parent command görünür |
| Node `fs.readFile*` | Hayır | Yalnız Node parent command görünür |
| Git’in açtığı individual files | Hayır | Yalnız git command |
| Module `sed` read | Evet | Explicit command olarak |
| Runtime internal AGENTS/config/skill metadata read | Hayır / belirsiz | Command event olmayabilir |
| Symlink resolution sonucu | Hayır | Validator bunu ayrıca resolve etmeliydi; çalışan oracle etmedi |
| Archive/decompression içindeki reads | Hayır | Parent extractor command görünür |
| Shell alias/function expansion | Güvenilir değil | Raw input alias’ı gösterebilir, resolved executable’ı değil |
| Environment-variable-expanded path | Genellikle yalnız unexpanded string | Shell expansion sonucu ayrı kaydedilmez |
| Command substitution child | Ayrı event garantisi yok | EXP oracle `$(` stringini bu nedenle yasakladı |

Ayrıca:

- EXP-005 validator’ın architecture ve containment branch’lerinde bilinen false-accept riskleri vardı.
- EXP-007 tasarımında `realpath`/symlink resolution istenmiş olsa da çalışan inline validator bunu tam uygulamadı.
- Kalıcı [test_cma_lazy_runtime.py](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/tests/test_cma_lazy_runtime.py:218) live process trace çalıştırmıyor.

# 10. EXP-006 RED analysis

**Baseline:** Aktif geniş router row ve geniş Graphify description; production candidate henüz yayınlanmamıştı.

**Zaten geçen probe:** Promptun kendisi exact shell command’ı ve exact final output’u dikte ediyordu:

```text
Run exactly: rg -n --fixed-strings ... AGENTS.md
```

**İspatlanmak istenen observable değişiklik:**

- candidate öncesi unwanted module/Graphify/non-`rg`,
- candidate sonrası aynı task’ta yalnız prescribed `rg`.

**Neden RED oluşmadı:** Model daha baseline’da prompttaki exact command’a uydu. Router/Graphify selection farkı observable trace’e yansımadı.

**Oracle mı yanlış, probe mu yetersiz, problem mi yoktu?**

- Static oracle amaçla uyumluydu ve RED üretti.
- Live oracle doğru şekilde fail-closed çalıştı.
- Live probe, natural routing davranışını ölçmek için yetersizdi çünkü çözüm yolunu input içinde önceden belirledi.
- Bu input için problem gerçekten gözlenmedi.
- Buradan problemin diğer inputlarda olmadığı sonucu çıkmaz; EXP-007 natural baseline aynı active state’te unwanted activation üretti.

Bir regression/failure’ın varlığını kanıtlamak için gerekli observable state şuydu:

1. completed lifecycle,
2. doğru task result,
3. inputun command seçimini dikte etmemesi,
4. raw trace’te unwanted module/Graphify veya non-allowed command,
5. candidate sonrası aynı task semantics ve oracle altında bu event’in yokluğu.

Bu, çözüm önerisi değil; behavioral causality iddiası kurmak için eksik kalan karşılaştırılabilir ölçümdür.

# 11. Security-boundary matrix

Buradaki durumlar aktif generic repository-read boundary içindir; component-local installer/record protections ayrı değerlendirilmiştir.

| Boundary | Durum | Kanıt |
|---|---|---|
| Repo root dışına read | **Allowed, gözlendi** | EXP-005 `~/.codex/...` ve memory okudu |
| Absolute path | **Allowed, gözlendi** | Skill/module/home absolute paths |
| `/tmp` | **Allowed, gözlendi** | EXP-004 corpus `/tmp` içindeydi |
| Home directory | **Allowed, gözlendi** | `~/.codex/skills`, module ve memory |
| `..` traversal | **Undefined production’da** | Temp oracle reddetmeye çalıştı; runtime guard yok |
| Symlink escape | **Undefined production’da** | Generic reader resolve/containment yok |
| Hidden files | **Allowed/tool-dependent** | EXP-005 `rg --hidden`; yalnız `.git` globu çıkarıldı |
| `.git` | **Default broad-scan exclusion, hard deny değil** | [GLOBAL_AGENTS_TEMPLATE.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/GLOBAL_AGENTS_TEMPLATE.md:146) |
| Gitignored files | **Tool/flags-dependent** | `rg` default ignore davranışı; production hard policy yok |
| Binary files | **Tool-dependent/undefined** | Genel size/type guard yok |
| Device files | **Undefined** | General reader regular-file check yapmıyor |
| FIFO | **Undefined** | Generic command boundary yok |
| Socket | **Undefined** | Aynı |
| Very large files | **Undefined** | Persistent byte/line cap yok |
| Recursive traversal | **Allowed fakat broad scans policy ile daraltılmaya çalışılıyor** | Exclusion list advisory |
| Archive files | **Broad scan’da default excluded; hard deny değil** | Policy satır 149–150 |
| Command substitution | **Shell tarafından mümkün; EXP oracle’da denied** | `$(` validator tarafından forbidden |
| Environment expansion | **Shell tarafından mümkün; production guard undefined** | Model command stringi zsh’ye gider |
| Shell redirection | **Runtime’da mümkün; EXP oracle’da denied** | Exact/generic validator |
| Additional writable dirs | **CLI configurable** | Installed `codex exec --help`; problarda kullanılmadı |
| Writes | **Probe sandbox ile denied/bounded** | Her task `--sandbox read-only` |
| Reads | **Read-only sandbox tarafından repo ile sınırlanmadı** | Home/system reads gözlendi |

Policy broad-scan exclusion’ları “by default” ifadesini kullanıyor; security denial değildir. [GLOBAL_AGENTS_TEMPLATE.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/GLOBAL_AGENTS_TEMPLATE.md:148)

# 12. Existing reusable enforcement primitives

| Primitive | Konum | Ne enforce ediyor | Bu problemle doğrudan ilişkisi |
|---|---|---|---|
| Secure record reader | `managed_location`, `open_managed_parent`, `read_bytes`; [source](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/skills/record-archive/scripts/record_archive.py:40) | Yalnız `docs/`/`governance/`; directory fd; `O_NOFOLLOW`; regular-file check | Gerçek bounded path reader, fakat yalnız record archive component’i |
| Project directory containment | `require_contained_directory`; [source](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/bin/codex-project-upgrade:117) | Managed project directories ve symlink escape | Upgrade workflow’ü; model reads değil |
| Runtime installer guard | `validate_managed_directory`, `assert_safe_target_path`; [source](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/bin/codex-user-install:250) | Runtime-home containment ve symlink rejection | Installer writes; repository read path’i değil |
| Claude SDK empty-tool boundary | `build_options`; [permissions.py](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/adapters/claude-agent-sdk/src/claude_agent_sdk_adapter/permissions.py:5) | Bash/Read/Grep dahil builtin denylist, boş allowed tools/MCP/settings | Optional Claude adapter; aktif Codex path’i değil |
| Codex read-only sandbox | External runtime CLI | Model shell commandlarının write yetkisini sınırlar | Read allowlist sağlamadığı gözlendi |
| `codex exec --json` | External runtime | Top-level event observability | Enforcement değil |
| CMA repository router | Markdown module | Candidate tool selection policy | Advisory; executable/path guard değil |
| EXP validators | Silinmiş disposable scripts, sessionlarda source fragments | Experiment-specific command/output oracle | Production primitive değil; bazı bilinen gaps var |
| Graphify corpus checks | Active Graphify skill body | Graph build’e özgü corpus/artifact davranışı | Generic repository reader değil |
| Historical ARK adapter | Repository’den rollback edilmiş | Artık aktif değil | Mevcut enforcement primitive sayılamaz |

Repository’nin onaylı minimal planı açıkça “No adapter, hook, installer, evidence wrapper, sandbox, or second runtime” diyor. [CMA_ARK_PLANNING_PROPOSAL.md](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/docs/CMA_ARK_PLANNING_PROPOSAL.md:49)

# 13. Potential enforcement-layer matrix

Bu tablo seçim veya öneri içermez; yalnız mevcut teknik yüzeyi sınıflandırır.

| Katman | Runtime enforcement mümkün mü? | Bypass yüzeyi | Mevcut test seam’i | Production blast radius |
|---|---|---|---|---|
| Prompt/policy | Hard enforcement değil | Model farklı command seçebilir | Static Markdown tests + live probes | Düşük–orta |
| Router metadata | Hard enforcement değil | Direct model command, başka skill | Static literal tests | Orta |
| Skill metadata | Aktivasyonu etkileyebilir; executable sınırı koymaz | Module/router/direct shell | Frontmatter static + live activation | Orta |
| Module selection | Context load’u etkiler; process guard değil | Tool doğrudan seçilebilir | Module contract tests | Orta |
| Planner/model | Deterministik enforcement kanıtlanmadı | Probabilistic seçim | Behavioral eval | Yüksek |
| Repository reader abstraction | Genel abstraction mevcut değil | Direct shell/interpreter/git | Component-local reader tests dışında yok | Yüksek |
| Command tool executor | External runtime’da top-level inspection teorik olarak mümkün | Compound command, interpreters, non-command internal APIs | JSONL command events | Yüksek |
| Subprocess wrapper | Repo-wide wrapper yok | Model doğrudan shell kullanıyor | `record_archive` component tests | Yüksek |
| Sandbox | OS/process seviyesinde writes enforce ediliyor | Read-only geniş read yüzeyi; internal runtime reads | CLI probes | Yüksek/global |
| OS/process boundary | Kernel düzeyinde enforce edilebilir | Platform farkları, internal runtime process’leri | Repository seam’i yok | Çok yüksek |
| Filesystem syscall boundary | Teknik olarak bütün file-open’ları görebilir | Repository’de implementasyon yok | Yok | Çok yüksek |
| Component-local safe reader | Kendi çağrıları için güçlü | Çağırmayan bütün yollar | `test_record_archive.py` | Düşük kendi scope’unda |

# 14. FACT / INFERENCE / UNKNOWN

## FACT

- Aktif repository-tools yapısı policy-only bir router’dır.
- Exact text/path için `rg`, architecture için Graphify yazılıdır.
- Router execution yetkisi vermediğini açıkça söyler.
- Kalıcı `bounded-reader` function/class/test yoktur.
- EXP-007 exact, filename ve known-file `/bin/zsh -lc` ile geçti.
- Shell wrapper tek başına reject edilmedi.
- Generic trace iki top-level command içerdi.
- Generic commandlar `rg`, `sed`, `ls`, `wc`, `&&` ve `;` içerdi.
- Generic final doğruydu.
- EXP-006 baseline exact prescribed command ile zaten geçti.
- Live probes `--sandbox read-only --ephemeral --json` kullandı.
- Absolute home ve `/tmp` reads gerçekleşti.
- JSONL top-level commands’ı gösteriyor; syscall/file-open trace üretmiyor.
- General repository read için repo-owned common wrapper yok.
- ARK runtime/adapter/hook yüzeyi rollback edilmiş durumda.
- Güncel policy/module/config/Graphify hash’leri deney öncesi değerlerle eşleşiyor.
- Güncel worktree’de yalnız `governance/EXPERIMENTS.md` değişik.

## INFERENCE

- Generic prompttaki düşük spesifiklik modelin heuristic search ve fallback üretme olasılığını artırdı.
- İlk `rg` pattern’inin sentinel-only README’de eşleşmemesi ikinci fallback command’ı tetikledi.
- Metadata/policy doğal dil değişiklikleri model selection’ını etkileyebilir, fakat process-level guarantee sağlamaz.
- Top-level command executor kısmi bir observation point’tir; tam repository-reader choke point değildir.
- EXP-003 token maliyetinin bir kısmı Graphify skill body context’inden kaynaklanmış olabilir; miktarı ayrıştırılamaz.

## UNKNOWN

- Codex runtime dispatcher/planner’ın exact scoring algoritması.
- Internal AGENTS/config/skill discovery’nin hangi file-open path’lerini kullandığı.
- Runtime internal reads’in JSONL dışında ayrı audit edilip edilmediği.
- Shell child/grandchild process’lerinin internal runtime’da ayrıca izlendiği.
- Read-only sandbox’ın tam filesystem read allow/deny modeli.
- Generic prompt tekrar çalıştırılsa aynı helper’ların seçilip seçilmeyeceği.
- Production-level `bounded-reader` için kabul edilen gerçek line/byte limiti.
- Symlink, device, FIFO, socket ve archive reads için ürün seviyesinde istenen policy.
- Bütün repository reads’i kapsayan external/runtime-owned gizli bir choke point olup olmadığı.
- EXP-003’ün temizlenen raw trace’indeki exact prompt ve dört skill-read command’ın tüm argv ayrıntıları.

# 15. Evidence index

## Authoritative repository records

- [EXP-007 record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:5)
- [EXP-006 record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:86)
- [EXP-005 record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:171)
- [EXP-004 record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:254)
- [EXP-003 record](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/governance/EXPERIMENTS.md:318)
- [Active repository-tools module source](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/registry/modules/CMA_REPO_TOOLS.md:1)
- [Global lazy-router policy](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/GLOBAL_AGENTS_TEMPLATE.md:124)
- [Static lazy-runtime tests](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/tests/test_cma_lazy_runtime.py:25)
- [Policy-only ARK/router decision](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/docs/CMA_ARK_PLANNING_PROPOSAL.md:1)

## Raw runtime evidence

- [EXP-004 baseline skill/module/rg trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:215)
- [EXP-005 baseline Graphify/module/memory/rg trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:866)
- [EXP-005 candidate module+rg trace](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:899)
- [EXP-006 prescribed baseline PASS](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1314)
- [EXP-007 natural behavioral RED](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1478)
- [EXP-007 exact PASS](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1507)
- [EXP-007 filename PASS](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1522)
- [EXP-007 known-file PASS](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1537)
- [EXP-007 generic-content failure](/Users/iyilmaz/.codex/sessions/2026/08/10/rollout-2026-08-10T06-51-30-019fe9cc-06eb-78b2-87fa-f4e227e2b688.jsonl:1556)

## Reusable source primitives

- [Secure record file reader](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/skills/record-archive/scripts/record_archive.py:40)
- [Record archive argv-based git subprocess](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/variants/codex/home/skills/record-archive/scripts/record_archive.py:428)
- [Project-upgrade containment](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/bin/codex-project-upgrade:117)
- [Runtime installer path guard](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/bin/codex-user-install:250)
- [Claude adapter tool denylist](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/adapters/claude-agent-sdk/src/claude_agent_sdk_adapter/permissions.py:5)
- [Claude adapter security limitation statement](/Users/iyilmaz/WebStorm/Codex-Multi-Agent/adapters/claude-agent-sdk/README.md:17)

# 16. Only unresolved questions requiring external input

Repository’den belirlenemeyen ürün/politika kararları şunlardır:

1. `bounded-reader` ürün seviyesinde yalnız executable/command-shape sınırı mı, yoksa kesin byte/line/file-count sınırı da mı taşımalıdır?
2. System policy/module/skill okumaları ile target repository okumaları aynı bütçe ve acceptance kapsamında mı sayılmalıdır?
3. `sed` known-file ve generic-content için ürün seviyesinde izinli primitive midir?
4. Metadata-only `ls` ve `wc`, hiç içerik okumasa bile reader boundary ihlali sayılmalı mıdır?
5. Git, Python, Node ve benzeri interpreter tabanlı reads ürün seviyesinde bütünüyle yasak mı, ayrıca sınırlı mı, yoksa use-case’e bağlı mı olmalıdır?
6. Read boundary yalnız repository root mu, yoksa açıkça gerekli global policy/skill paths ve `/tmp` fixture’ları da kapsamalı mıdır?
7. Symlink, hidden, gitignored, binary, archive, device/FIFO/socket ve large-file davranışları için beklenen resmi allow/deny politikası nedir?
8. Desteklenmesi gereken platformlar yalnız macOS/zsh mi, yoksa Linux ve farklı shell/runtime’lar da mı?
9. Kabul edilebilir process count, file count, byte/line miktarı ve latency sınırları nedir?
10. Runtime internal context/module discovery okumalarının audit kapsamına dahil edilmesi ürün gereksinimi midir?


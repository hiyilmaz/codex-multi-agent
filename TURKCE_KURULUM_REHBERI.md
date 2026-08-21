# Türkçe Kurulum Rehberi

Bu rehber iki kullanım içindir:

1. Yeni bir bilgisayarda Codex kullanıcı ortamını sıfırdan kurmak.
2. Bir proje içine Codex proje dosyalarını eklemek.

Aktif yapı basittir:

```text
variants/
  config.toml
  codex/home/
  claude/home/
  opencode/home/

~/.codex/
  AGENTS.md
  config.toml
  agents/
  skills/
  registry/

<project>/
  AGENTS.md
  .codex/config.toml
  .codex/prompts/fill-project-configuration.md
```

Tüm varyantlar, iddia, öneri, önemli karar ve tartışmalı konularda
`Evidence-First Objectivity` davranışını kullanır. Sonuç kullanıcıyı memnun
etmeye göre değil, doğrulanabilir ve mümkünse bağımsız kanıtlara göre verilir;
karşıt kanıtlar, riskler, kaynak çatışmaları ve belirsizlik açıkça belirtilir.
Bu kural rutin kodlama, dosya düzenleme, çeviri veya operasyon görevlerinde
otomatik araştırma zorunluluğu oluşturmaz.

## 1. Sıfırdan Kurulum

Önce bu repo bilgisayarda olmalı:

```bash
cd /path/to/Codex-Multi-Agent
```

En kolay yöntem kurulum sihirbazını çalıştırmaktır:

```bash
bin/codex-setup
```

Değişiklik yapan genel kurulum için Node.js 22 veya üzeri ve `npx` zorunludur.
Yardım ve varyant listeleme komutları bu ön kontrolden bağımsız, salt-okunur
çalışır.

Sihirbaz şunları sorar:

- tüm etkin modellerin kurulup kurulmayacağı; **Evet** seçilirse her model
  sorusuz uygulanır, **Hayır** seçilirse modeller tek tek sorulur
- runtime hedef dizini
- kullanıcı-global template kurulumu
- kurulacak runtime versiyonu
- mevcut dosyaların ezilip ezilmeyeceği
- YOLO modu
- hata, izin, tamamlandı ve karar bekleme mesajları
- istenirse proje içine Codex yapısı kurulumu
- varsayılanı **Evet** olan resmi `npx ctx7 setup` adımı

Context7 kimlik doğrulamayı ve algılanan Claude Code, OpenCode ve Codex için
global MCP, rule ve skill değişikliklerini süreç kullanıcısının `HOME` dizini
altında kendisi yönetir. Özel `--runtime-home` bu Context7 hedeflerini
değiştirmez. CMA API anahtarını komut argümanına eklemez; Context7 başarısız
olursa sihirbaz da aynı hata koduyla tamamlanmadan çıkar. Context7 en son
çalıştığı için daha önce tamamlanan CMA yazımları otomatik geri alınmaz.

Kullanıcı-global Codex ortamını kur:

```bash
bin/codex-user-install
```

Doğrudan değişiklik yapan `codex-user-install` çağrıları da Node.js 22 veya
üzeri ve `npx` gerektirir. Bu komut tek başına `npx ctx7 setup` çalıştırmaz;
interaktif çoklu-agent Context7 adımı genel `codex-setup` sihirbazına aittir.

Belirli bir versiyonu kur:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant claude
bin/codex-user-install --variant opencode
```

Kurulum sırasında template içindeki kaynak pathler hedef `--runtime-home`
dizinine göre yazılır.

Hedef tam olarak `$HOME/.codex` ise kurulum template tamamlandıktan sonra
`bin/codex-native-activate` komutunu çalıştırır. Bu işlem 10 korumalı aracı
eklemeli olarak etkinleştirir; Context7 required fakat lazy kalır, cplt
explicit-only kalır ve xcodebuildmcp kapalı tutulur. Özel runtime hedefleri ile
Native Claude ve OpenCode aynı 10 skill'i kendi resmi kullanıcı dizinlerine
eklemeli olarak projekte eder. Ardından ilgili istemciyi yeniden başlat veya yeni
bir oturum aç.

Varsayılan hedefler:

```text
codex   -> $HOME/.codex
claude  -> $HOME/.claude
opencode -> $HOME/.config/opencode
```

Claude launcher dosyası kurulumdan sonra şurada olur:

```text
<runtime-home>/bin/llm-claude
<runtime-home>/bin/llm-opencode
```

OpenCode, resmi kullanıcı skill dizini olan `~/.config/opencode/skills`
üzerinden etkinleşir. İlgisiz yapılandırma ve kimlik durumunu korur; yönetilen
skill hedefinde symlink veya farklı içerik varsa fail-closed davranır.
Provider/model seçmez, plugin veya bağımlılık kurmaz ve giriş yapmaz.
Yapılandırmayı model çağrısı olmadan `opencode mcp list` ve
`opencode debug config` ile doğrula.

Claude kurulumu varsayılan olarak doğal kullanıcı-global `~/.claude` dizinine
uygulanır. Mevcut `CLAUDE.md` bayt bayt korunur; özel bir kopyası ve kontrollü
birleştirme promptu üretilir;
mevcut `settings.json` değiştirilmez ve native hedefte `--force` reddedilir.
`llm-claude`, `CLAUDE_CONFIG_DIR` değerini kurulduğu runtime dizinine ayarlayıp
önceden kurulmuş native `claude` komutunu çalıştırır. Agent SDK kurmaz veya
giriş yapmaz. İzole testler için açık bir `--runtime-home` verilebilir.

Native aktivasyon, CMA aday politikasını `~/.claude/registry/CMA_GLOBAL.md`
olarak kurar; `~/.claude/CLAUDE.md` içine otomatik import eklemez. Mevcut
talimatın özel kopyası ve yalnız dosya yollarını içeren AI promptu şuralara
yazılır:

```text
~/.claude/backups/instruction-merge/
~/.claude/prompts/merge-existing-instructions.md
```

Farklı içerikte mevcut bir CMA-managed dosya, güvenli olmayan symlink, eksik
kaynak veya kopyalama/yedekleme hatası aktivasyonu durdurur. İşlem sırasında
hata oluşursa kısmi kurulum geri alınır. Eski izole Claude runtime dizini
silinmez veya değiştirilmez.

Bu komut şunları hazırlar:

```text
~/.codex/AGENTS.md
~/.codex/config.toml
~/.codex/agents/
~/.codex/skills/
~/.codex/registry/
~/.codex/rules/
```

Varsayılan olarak mevcut dosyaları ezmez.

Mevcut dosyaları bilinçli olarak template ile değiştirmek istersen:

```bash
bin/codex-user-install --force
```

Bu seçenek yalnız politika dışındaki template-managed Codex dosyaları içindir;
mevcut global talimat dosyası yine korunur ve birleştirme promptu üretilir.
Native Claude aktivasyonunda `--force`
bilerek reddedilir. Etkileşimli Claude kurulumunda “Mevcut template-managed
dosyalar ezilsin mi?” sorusuna `n` yanıtını ver.

## 2. Başka Bilgisayarda Kurulum

### Ubuntu 24 üzerinde bağımsız `codex-tools`

Depoyu Ubuntu 24 makineye kopyaladıktan sonra Python 3.11 ve `uv` hazır
olmalıdır. Araç paketi CMA çalışma zamanından bağımsız kurulabilir:

```bash
cd /path/to/Codex-Multi-Agent
uv tool install ./tools/codex-tool-installer
codex-tools --version
codex-tools check
```

CMA içinde MCP ayarlarının sahibi CMA olarak kalır:

```bash
bin/cma-tools check
bin/cma-tools dry-run
bin/cma-tools install
```

Kurulum sihirbazına isteğe bağlı eklemek için:

```bash
bin/codex-setup --variant codex --tools-mode check
bin/codex-setup --variant codex --tools-mode install
```

Varsayılan `--tools-mode skip` değeridir. CMA adaptörü MCP kayıtlarını yalnızca
doğrular; değiştirmez. Bağımsız `codex-tools` kullanımı ise varsayılan
`manage` modunda yalnızca eksik veya kendi işaretiyle sahip olduğu MCP
tablolarını yönetir ve kullanıcıya ait isim çakışmasında durur.

Yeni bilgisayarda bu repo aynı şekilde alınır:

```bash
git clone <repo-url> Codex-Multi-Agent
cd Codex-Multi-Agent
```

Sonra:

```bash
bin/codex-user-install
```

Bu kadar. `codex` runtime `~/.codex` altında, `claude` runtime ise
doğal kullanıcı-global `~/.claude` altında çalışır. Repo içindeki
`variants/` dizini sadece taşınabilir kurulum kaynaklarını ve varsayılan
versiyon config dosyasını taşır.

## 3. Yeni Proje veya Eklemeli Varyant Kurulumu

Yeni veya mevcut bir projeye Codex proje yapısını eklemek için:

```bash
cd /path/to/Codex-Multi-Agent
bin/codex-project-init /path/to/project
```

Yeni projede komut ortak proje yüzeyini oluşturur. Mevcut projede init eklemeli
çalışır; `AGENTS.md` dosyasını korur, ortak promptları ve özelleştirilmiş
dosyaları değiştirmez. Birden fazla runtime varyantı aynı projede birlikte
kullanılabilir ve `.codex/template-state.json` içinde birlikte kaydedilir.
`--variant` verilmezse önce tüm etkin modeller sorulur: **Evet** tümünü ekler,
**Hayır** ise her varyantı tek tek seçtirir. `--variant` mevcut tek-varyant
komut sözleşmesini korur.

Ortak proje yapısını yalnız bilinçli olarak sıfırlamak için:

```bash
bin/codex-project-init --reset --variant codex /path/to/project
```

Reset, çakışan dosyaları onaydan önce listeler ve özel arşive taşır. Yeni Codex
projesi şunları oluşturur:

```text
<project>/AGENTS.md
<project>/.codex/config.toml
<project>/.codex/prompts/fill-project-configuration.md
```

`--variant claude` seçildiğinde yalnızca `@AGENTS.md` içeren
`<project>/CLAUDE.md` ve `<project>/.claude/settings.json` eklenir. Diğer proje
ve `.claude` içeriğine dokunulmaz.

`--variant opencode` seçildiğinde `.opencode/opencode.json` eklenir. Mevcut
Codex yapılandırması, `.opencode/plugins`, paket metadata dosyaları ve
diğer kardeş içerikler korunur.

Mevcut `AGENTS.md` algılanırsa `.codex/archive/instruction-merge/` altında özel,
içerik-adresli bir kopya ve
`.codex/prompts/merge-existing-instructions.md` oluşturulur. Claude seçiliyken
mevcut `CLAUDE.md` için ayrıca
`.codex/prompts/merge-existing-claude-instructions.md` yazılır. Kullanıcı bu
promptu AI modelinde çalıştırır; AI yalnız önerilen diff ve çatışma raporu
üretir, dosyaları otomatik değiştirmez.
Hedef prompt adında farklı bir dosya zaten varsa korunur; yeni prompt içerik
özeti son ekiyle yanına yazılır ve kesin yolu komut çıktısında gösterilir.

Yalnız `--reset` sırasında çakışan dosyalar şuraya arşivlenir:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS-PID/
```

Zaten init edilmiş projeyi resetlemeden güncellemek için:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

Init sırasında template sürümü, aktif varyantlar ve managed dosya hash'leri
`.codex/template-state.json` içine kaydedilir. Upgrade mevcut `AGENTS.md`
değerlerini ve projeye özel eklemeleri korur; yalnızca eksik baseline alanlarını
ekler. Hash'i değişmiş prompt/config dosyalarının üzerine yazmaz ve bunları
project-owned olarak işaretler.

Dry-run varsayılandır ve hiçbir dosya yazmaz. `--apply` yalnızca incelenen planı
uygular. Değiştirilecek mevcut dosyalar şuraya arşivlenir:

```text
<project>/.codex/archive/upgrade-YYYYMMDD_HHMMSS_microseconds/
```

## 4. Proje AGENTS.md Doldurma

Kurulumdan sonra şu dosyadaki prompt çalıştırılır:

```text
<project>/.codex/prompts/fill-project-configuration.md
```

Bu prompt projenin `AGENTS.md` dosyasındaki sadece `Project Configuration`
bloğunu doldurur.

## 5. Mevcut Projeyi Hızlı Kontrol

Projede eski dış katman referansı kalmış mı kontrol et:

```bash
cd /path/to/project
rg -n "ECC|ECC_ROOT|Codex-ECC|everything-claude-code|codex-ecc" AGENTS.md .codex README.md docs bin scripts
```

Sonuç çıkmıyorsa proje yeni sade modele uyumludur.

## 6. Günlük Kullanım Mantığı

Günlük çalışma kaynağı:

```text
~/.codex/AGENTS.md
~/.codex/agents/
~/.codex/skills/
~/.codex/registry/
project/AGENTS.md
```

Zorunlu orchestration zinciri korunur:

```text
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

Proje `AGENTS.md` içinde orchestration davranışı şu alanla belirlenir:

```text
ORCHESTRATION_MODE: ask-approval
```

Geçerli değerler:

- `skip`: varsayılan olarak orchestration kullanılmaz.
- `ask-approval`: zincir ana planda açıklanır ve ciddi işlerde yalnızca ilk ana
  plan onayı alınır.
- `run-chain`: proje veya kullanıcı açıkça yetki verdiyse ciddi işlerde zincir
  başlatılır; aktif tool politikası ayrıca onay istiyorsa önce onay alınır.

### Ana Plan Yürütme

CMA doğrulanmış ana plan için başlangıçta bir kez açık kullanıcı onayı ister.
Onaydan sonra planlanmış fazları ve alt görevleri görev sınırlarında yeniden
onay istemeden tamamlar. Ana liste güncellemeleri, yardımcı görevler, önerilen
görevler ve nihai başarı/başarısızlık sonucu raporlanır. Destructive ve
High/Critical işlemler için ayrı açık onay zorunluluğu devam eder. İlk plan
onayı, planda açıklanan destructive olmayan Low/Medium işleri ve planlanmış
orkestrasyonu kapsar.
Onaylı plan dışında bulunan işler yardımcı görev listesinde tutulur ve ana
görevin devamı için zorunlu değilse uygulanmaz. Zorunlu bir plan sapması, plan
değiştirilmeden önce raporlanır ve onaylanır. Önerilen görevler ayrı raporlanır
ve ana görev listesine hiçbir zaman otomatik eklenmez.

`orchestration-gate` skill'i bu kararın verilmesi için kullanılır.
`tdd-workflow` her runtime varyantında bulunur ve test-first geliştirme akışını
uygular. `openai-docs` gibi göreve özel skill'ler yalnızca proje için ilgili ve
aktif Codex oturumunda mevcut olduklarında eklenir.

Yeni skill veya agent gerektiğinde `skill-agent-governor` sorumludur.

## 7. Kısa Komut Özeti

Soru-cevap kurulum sihirbazını çalıştır:

```bash
bin/codex-setup
```

Kullanıcı ortamı kur:

```bash
bin/codex-user-install
```

Kullanıcı ortamını belirli versiyonla kur:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant opencode
bin/codex-user-install --variant opencode
```

Kullanıcı ortamını zorla yenile:

```bash
bin/codex-user-install --force
```

Proje içine Codex yapısı kur:

```bash
bin/codex-project-init /path/to/project
```

Init edilmiş projeyi güncelle:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

## 8. YOLO Modu

Kurulum sihirbazı YOLO modunu sorar.

YOLO açık olsa bile şu işlemler her zaman kullanıcı onayı ister:

```text
DROP, DELETE *, TRUNCATE, rm -rf, git reset --hard, git push --force
dependency ekleme
API contract değişikliği
DB schema değişikliği
auth/security kodu değişikliği
```

Yani YOLO modu destructive veya yüksek riskli işlemlerde onayı kaldırmaz.

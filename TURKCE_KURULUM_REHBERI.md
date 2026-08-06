# Türkçe Kurulum Rehberi

Bu rehber iki kullanım içindir:

1. Yeni bir bilgisayarda Codex kullanıcı ortamını sıfırdan kurmak.
2. Bir proje içine Codex proje dosyalarını eklemek.

Aktif yapı basittir:

```text
variants/
  config.toml
  codex/home/
  dolphin/home/
  claude/home/

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

## 1. Sıfırdan Kurulum

Önce bu repo bilgisayarda olmalı:

```bash
cd /path/to/Codex-Multi-Agent
```

En kolay yöntem kurulum sihirbazını çalıştırmaktır:

```bash
bin/codex-setup
```

Sihirbaz şunları sorar:

- runtime hedef dizini
- kullanıcı-global template kurulumu
- kurulacak runtime versiyonu
- mevcut dosyaların ezilip ezilmeyeceği
- YOLO modu
- hata, izin, tamamlandı ve karar bekleme mesajları
- istenirse proje içine Codex yapısı kurulumu

Kullanıcı-global Codex ortamını kur:

```bash
bin/codex-user-install
```

Belirli bir versiyonu kur:

```bash
bin/codex-user-install --variant codex
bin/codex-user-install --variant dolphin
bin/codex-user-install --variant claude
```

Kurulum sırasında template içindeki kaynak pathler hedef `--runtime-home`
dizinine göre yazılır.

Varsayılan hedefler:

```text
codex   -> $HOME/.codex
dolphin -> $HOME/.llm-runtimes/dolphin
claude  -> $HOME/.claude
```

Dolphin launcher kurulumdan sonra şurada olur:

```text
<runtime-home>/bin/llm-dolphin
<runtime-home>/bin/llm-claude
```

Claude kurulumu varsayılan olarak doğal kullanıcı-global `~/.claude` dizinine
uygulanır. Mevcut `CLAUDE.md` yedeklenip tek CMA importu eklenerek korunur;
mevcut `settings.json` değiştirilmez ve native hedefte `--force` reddedilir.
`llm-claude`, `CLAUDE_CONFIG_DIR` değerini kurulduğu runtime dizinine ayarlayıp
önceden kurulmuş native `claude` komutunu çalıştırır. Agent SDK kurmaz veya
giriş yapmaz. İzole testler için açık bir `--runtime-home` verilebilir.

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

## 2. Başka Bilgisayarda Kurulum

Yeni bilgisayarda bu repo aynı şekilde alınır:

```bash
git clone <repo-url> Codex-Multi-Agent
cd Codex-Multi-Agent
```

Sonra:

```bash
bin/codex-user-install
```

Bu kadar. `codex` runtime `~/.codex` altında çalışır. `dolphin` runtime
varsayılan olarak `~/.llm-runtimes/dolphin`, `claude` runtime ise
doğal kullanıcı-global `~/.claude` altında çalışır. Repo içindeki
`variants/` dizini sadece taşınabilir kurulum kaynaklarını ve varsayılan
versiyon config dosyasını taşır.

## 3. Yeni Proje İçine Kurulum

Yeni veya mevcut bir projeye Codex proje yapısını eklemek için:

```bash
cd /path/to/Codex-Multi-Agent
bin/codex-project-init /path/to/project
```

Komut onay ister. Onaydan sonra şunları oluşturur:

```text
<project>/AGENTS.md
<project>/.codex/config.toml
<project>/.codex/prompts/fill-project-configuration.md
```

`--variant claude` seçildiğinde ayrıca yalnızca `@AGENTS.md` içeren
`<project>/CLAUDE.md` ve `<project>/.claude/settings.json` oluşturulur. Mevcut
Claude dosyaları onaydan önce listelenir; onaylanan reset sırasında arşivlenir.
Diğer `.claude` içeriğine dokunulmaz.

Eğer projede eski Codex dosyaları varsa, bunları şuraya arşivler:

```text
<project>/.codex/archive/init-YYYYMMDD_HHMMSS/
```

Zaten init edilmiş projeyi resetlemeden güncellemek için:

```bash
bin/codex-project-upgrade --dry-run /path/to/project
bin/codex-project-upgrade --apply /path/to/project
```

Init sırasında template sürümü, variant ve managed dosya hash'leri
`.codex/template-state.json` içine kaydedilir. Upgrade mevcut `AGENTS.md`
değerlerini ve projeye özel eklemeleri korur; yalnızca eksik baseline alanlarını
ekler. Hash'i değişmiş prompt/config dosyalarının üzerine yazmaz ve bunları
project-owned olarak işaretler.

Dry-run varsayılandır ve hiçbir dosya yazmaz. `--apply` yalnızca incelenen planı
uygular. Değiştirilecek mevcut dosyalar şuraya arşivlenir:

```text
<project>/.codex/archive/upgrade-YYYYMMDD_HHMMSS/
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
- `ask-approval`: ciddi işlerde zincir başlatılmadan önce onay istenir.
- `run-chain`: proje veya kullanıcı açıkça yetki verdiyse ciddi işlerde zincir
  başlatılır; aktif tool politikası ayrıca onay istiyorsa önce onay alınır.

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
bin/codex-user-install --variant dolphin
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

# Coding Conventions & Git Workflow — SIGAP

## Git Branching
main → production-ready, protected
dev → integration branch, PR target
feature/xxx → fitur baru (dari dev)
fix/xxx → bugfix
chore/xxx → non-functional changes
docs/xxx → dokumentasi saja

text

**Contoh nama branch**:
- `feature/uss-engine-v2`
- `fix/alert-false-positive`
- `docs/update-api-reference`

---

## Commit Message (Conventional Commits)
<type>(<scope>): <deskripsi singkat>

[optional body]

text

**Types**: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`

**Contoh**:
feat(uss): tambah normalisasi indikator per kota
fix(auth): perbaiki refresh token expired logic
docs(api): update endpoint simulator

text

---

## Python (Backend)

- **Formatter**: `black` (line length 88)
- **Linter**: `ruff`
- **Type hints**: wajib untuk semua fungsi publik
- **Docstring**: Google style untuk service methods
- **Async**: semua DB call dan HTTP call harus `async`

```python
# ✅ Benar
async def compute_uss(kelurahan_id: UUID, db: AsyncSession) -> USSResult:
    """Compute Urban Stress Score for a given kelurahan.
    
    Args:
        kelurahan_id: UUID of the target kelurahan.
        db: Async database session.
    
    Returns:
        USSResult with breakdown per dimension.
    
    Raises:
        KelurahanNotFoundError: If kelurahan_id does not exist.
    """
    ...

# ❌ Salah
def compute_uss(id, db):
    ...
```

---

## TypeScript (Frontend)

- **Formatter**: Prettier
- **Linter**: ESLint (Airbnb config)
- **No `any`** kecuali benar-benar tidak bisa dihindari dan wajib diberi komentar alasan
- **Component**: Functional components + hooks only, no class components
- **Naming**: PascalCase untuk components, camelCase untuk variabel/fungsi

---

## PR Rules

- Minimal 1 reviewer sebelum merge ke `dev`
- PR harus include: deskripsi, screenshots/output (untuk UI), dan hasil test
- Semua CI checks harus hijau sebelum merge
- Squash merge untuk `feature/*` ke `dev`
- No force push ke `dev` dan `main`
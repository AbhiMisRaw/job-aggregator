# Development Workflow

## Branches

- main
- staging
- feature/<name>
- fix/<name>
- docs/<name>

## Workflow

1. Create a feature/fix branch from main.
2. Implement the change.
3. Test locally.
4. Review the git diff.
5. Commit the changes.
6. Merge into main.
7. Delete the temporary branch.

## Commit Convention

feat: New functionality
fix: Bug fix
refactor: Code restructuring
docs: Documentation
chore: Maintenance

Examples:

feat: add job search API
fix: handle invalid JWT token
refactor: simplify job service


## NOTE

`staging:`
- No direct pushes
- Changes come through PRs from temporary branches

`main:`
- No direct pushes
- Only staging can be merged into it
- PR required

```
Write code
   ↓
isolated branch
   ↓
PR
   ↓
staging
   ↓
test
   ↓
PR
   ↓
main
```

## Definition of Done

- Feature works locally
- Tests pass
- Git diff reviewed
- No secrets committed
- Documentation updated when required
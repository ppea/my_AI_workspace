The brainstorm → writing-plans workflow produces design docs and implementation plans
in docs/plans/, but these were never tracked anywhere. There was no way to know which
plans were in-flight, being implemented, or completed. Each project had orphaned plan
files with no lifecycle visibility.

This change adds automatic OpenSpec registration as step 7 of the brainstorming skill.
After every writing-plans invocation, the resulting design doc and implementation plan
are copied into a self-contained OpenSpec change. This enables the full lifecycle:
brainstorm → OpenSpec change created → /opsx-apply → /opsx-archive.
The approach uses a local skill override (skills/custom/brainstorming/SKILL.md) rather
than patching the vendor submodule, keeping the vendor clean and enabling easy future updates.

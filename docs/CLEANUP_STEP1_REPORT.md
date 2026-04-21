# Step 1 Cleanup Report (Archive-only)

## Scope

- Archive overlapping/legacy launch files only.
- No hard deletes.
- Keep runtime/build/test references safe.

## Archived files

- `src/gp7_gazebo_classic/launch/gazebo.launch.py` -> `src/gp7_gazebo_classic/launch/legacy/gazebo.launch.py`
- `src/gp7_gazebo_classic/launch/gazebo1.launch.py` -> `src/gp7_gazebo_classic/launch/legacy/gazebo1.launch.py`
- `src/gp7_bringup/launch/display_xml.xml` -> `src/gp7_bringup/launch/legacy/display_xml.xml`

## Deleted files

- None.

## Documentation/reference updates

- Updated `src/gp7_gazebo_classic/README.md`:
  - `gazebo_display.launch.py` and `sim_moveit.launch.py` marked as current launches.
  - `launch/legacy/*` listed as archived variants.
- Updated `src/gp7_bringup/README.md`:
  - `display_xml.xml` path updated to `launch/legacy/display_xml.xml`.

## Retained suspicious files and why

- `src/gp7_gazebo_classic/launch/legacy/gazebo.launch.py`
  - Retained for regression/reference while moving to a single primary display and sim-moveit path.
- `src/gp7_gazebo_classic/launch/legacy/gazebo1.launch.py`
  - Retained as alternate historical controller sequencing reference.
- `src/gp7_bringup/launch/legacy/display_xml.xml`
  - Retained legacy XML reference; modern path is `display.launch.py`.

## Safety check

- No files removed from install tree categories (`launch/` still installed recursively by CMake).
- No real-robot launch files modified.
- No fake-hardware pipeline files modified.

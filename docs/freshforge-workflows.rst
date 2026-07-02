FreshForge Workflows
====================

Phase 17 adds the first TFL6-owned FreshForge workflow document:

.. code-block:: text

   workflows/freshforge/tfl6_model_build_workflow.yaml
   workflows/freshforge/tfl6_materialization_workflow.yaml

The graph uses the generic FEMIC provider namespace. TFL6 does not define a
``tfl6.*`` provider in this phase. If later workflow nodes need TFL6-specific
script orchestration, that implementation should live in a TFL6-owned adapter
package rather than in FEMIC core.

Install FreshForge
------------------

FreshForge is optional for FEMIC. Install it through the FEMIC FreshForge extra
from the parent FEMIC checkout:

.. code-block:: bash

   python -m pip install -e ".[freshforge]"

Model-Build Workflow
--------------------

Run these commands from the TFL6 instance root:

.. code-block:: bash

   freshforge providers
   freshforge validate workflows/freshforge/tfl6_model_build_workflow.yaml
   freshforge inspect workflows/freshforge/tfl6_model_build_workflow.yaml
   freshforge plan workflows/freshforge/tfl6_model_build_workflow.yaml

The expected graph order is:

1. validate case;
2. geospatial preflight;
3. compile upstream FEMIC inputs;
4. BTC/post-TIPSY bundle processing;
5. Patchworks XML/fragments export;
6. Patchworks preflight; and
7. Matrix Builder.

Phase 17 validates and plans the orchestration surface. The current FreshForge
release does not expose ``freshforge run --dry-run``; a full explicit
``freshforge run`` through BTC and Patchworks is a later acceptance lane.

Materialization Workflow
------------------------

Phase 18 adds a parent-checkout materialization workflow:

.. code-block:: text

   external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml

Run these commands from the parent FEMIC checkout root:

.. code-block:: bash

   freshforge providers
   freshforge validate external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml
   freshforge inspect external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml
   freshforge plan external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml

``freshforge plan`` is the non-mutating preview. The explicit run command
performs real submodule, Python environment, DataLad, and git-annex work:

.. code-block:: bash

   freshforge run external/femic-tfl6-instance/workflows/freshforge/tfl6_materialization_workflow.yaml --workdir runtime/freshforge --namespace tfl6/materialization --json

Boundaries
----------

- FreshForge validation, inspection, and planning are the primary Phase 17
  checks.
- Workflow-declared artifacts are metadata until the launched FEMIC commands
  actually create or update them.
- The Phase 18 materialization workflow is the first FreshForge path that
  materializes TFL6 DataLad/git-annex content.
- Runtime outputs under ``runtime/freshforge/`` are local/generated and should
  not be tracked.

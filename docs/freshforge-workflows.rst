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

Phase 19 promotes the model-build workflow to an executable parent-checkout
acceptance lane. Use the parent FEMIC discovery helper first:

.. code-block:: bash

   python -m femic freshforge workflows list
   python -m femic freshforge workflows commands external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml

Run these checks from the parent FEMIC checkout root:

.. code-block:: bash

   freshforge providers
   python -m femic instance validate-spec --instance-root external/femic-tfl6-instance --spec config/rebuild.spec.yaml
   freshforge validate external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
   freshforge inspect external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml
   freshforge plan external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml

The expected graph order is:

1. validate case;
2. geospatial preflight;
3. compile upstream FEMIC inputs;
4. BTC/post-TIPSY bundle processing;
5. Patchworks XML/fragments export;
6. Patchworks preflight; and
7. Matrix Builder.

``freshforge plan`` is the non-mutating preview. The explicit run command
executes FEMIC, BTC, and Patchworks stages:

.. code-block:: bash

   freshforge run external/femic-tfl6-instance/workflows/freshforge/tfl6_model_build_workflow.yaml --workdir runtime/freshforge --namespace tfl6/model-build --json

If the TFL6 submodule is thin or incomplete, run the materialization workflow
before running the model-build workflow.

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

- FreshForge validation, inspection, and planning remain non-mutating checks.
- The model-build ``freshforge run`` command executes FEMIC, BTC, and
  Patchworks stages when run explicitly.
- Workflow-declared artifacts are metadata until the launched FEMIC commands
  actually create or update them.
- The Phase 18 materialization workflow is the first FreshForge path that
  materializes TFL6 DataLad/git-annex content.
- Runtime outputs under ``runtime/freshforge/`` are local/generated and should
  not be tracked.

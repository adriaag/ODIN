# Intent Specification to Workflow Generation Framework

## Requirements
- Python (3.10 or higher)
    - List of packages in `requirements.txt` (can be installed with `pip install -r requirements.txt`)
        - PySHACL packages available at [DTIM PySHACL repo](https://github.com/dtim-upc/pySHACL)(already specified in `requirements.txt`')
- Node.js (specific for the demo)
    - List of packages in `package.json` (install with `npm install`)

## Directory Structure
- `common/`: contains code for definitions of base elements of the ontology and workflow generation, namely the namespaces and the main ontology incorporating the different layers and dataset annotation. 
- `dataset_annotator/`: contains code for annotating tabular datasets with ontology terms. More details in this [section](#dataset-annotator).
- `ontology_populator/`: contains code for generating the entire ontology. More details in this [section](#ontology-populator).
- `modified-ontologies/`: contains the different layers composing the ontology used in the project, divided in the following files:
    - [`tbox.ttl`](./modified-ontologies/tbox.ttl): terminological schema layer of the ontology.
    - [`cbox.ttl`](./modified-ontologies/cbox.ttl): taxonomical vocabulary layer of the ontology.
    - [`abox.ttl`](./modified-ontologies/abox.ttl): assertional layer of the ontology.
- `pipeline_generator/`: contains code for workflow generation. More details in this [section](#pipeline-generator).
- `pipeline_translator/`: contains code for translating generated workflows into executable KNIME workflows. Usage details in this [section](#pipeline-translator).
- `demo/`: contains code for the graphical demo. More details in this [section](#demo).
- `experimental_runs/`: contains code for running the benchmarking experiments. More details in [section](#experimental-runs).



## Dataset Annotator
The script in [`annotator.py`](./dataset_annotator/annotator.py) annotates all the csv-formatted tabular datasets in [`datasets`](./dataset_annotator/datasets) with ontology terms outputting the annotated datasets into the [`annotated_datasets](./dataset_annotator/annotated_datasets) directory.

The script in [`knime_annotator.py`](./dataset_annotator/knime_annotator.py) performs the same task as [`annotator.py`](./dataset_annotator/annotator.py) with the datatype definitions being compliant with the KNIME engine datatype defintions. 

To run the the dataset annotation:
```bash
cd dataset_annotator
python < annotator.py or knime_annotator.py >
```

## Ontology Populator

### TBOX Generator
The code in [`tbox_generator.py`](./ontology_populator/tbox_generator.py) generates the TBox of the ontology and stores it in the [`modified-ontologies`](./modified-ontologies/) directory.

```bash
cd ontology_populator
python3 tbox_generator.py
```

### CBOX Generator
The CBox of the ontology is generated using the code in [`cbox_generator.py`](./ontology_populator/cbox_generator.py) and stored in the  [`modified-ontologies`](./modified-ontologies/) directory.

```bash
cd ontology_populator
python3 cbox_generator.py
```

The CBox is divided into two levels:

#### Engine-Agnostic CBOX
This level contians the following elements:
- Tasks: specified in the [`cbox_generator.py`](./ontology_populator/cbox_generator.py) script.
- Algorithms: specified in the [`cbox_generator.py`](./ontology_populator/cbox_generator.py) script.
- Data Specifications: specified in the [`cbox_generator.py`](./ontology_populator/cbox_generator.py) script.
- Shapes: defined in the [`cbox_generator.py`](./ontology_populator/cbox_generator.py) script.
- Implementations: the subclasses are specified in the [`tbox_generator.py`](./ontology_populator/tbox_generator.py) script (`LearnerImplmentation`, `ApplierImplementation`, ...etc). The definition of the Implementation class is in [`implmentation.py`](./ontology_populator/implementations/core/implementation.py).
- Components: the subclasses are specified in the [`tbox_generator.py`](./ontology_populator/tbox_generator.py) script (`LearnerComponent`, `ApplierComponent`, ...etc). The definition of the Component class is in [`component.py`](./ontology_populator/implementations/core/component.py).
- Transformations: the definitions of all the transformation classes are in [`transformation.py`](./ontology_populator/implementations/core/transformation.py). 
- Rules: the rules are defined within the components. An example can be found in the KNIME [`normalization.py`](./ontology_populator/implementations/knime/normalization.py) instance.

#### Engine-Specific CBOX
- Parameters: the definition of the Parameter concept is in [`parameter.py`](./ontology_populator/implementations/core/parameter.py). Additionally, an engine-specific (KNIME) subclass is also defined in [`knime_implementation.py`](./ontology_populator/implementations/knime/knime_implementation.py) encoding engine-specific implementation information.
- Implementations: an engine-specific (KNIME) subclass is defined in [`knime_implementation.py`](./ontology_populator/implementations/knime/knime_implementation.py) encoding engine-specific implementation information.
- Additional Entities: some engine-specific classes may need to be defined depending on the engine requirements. For example, `KnimeBundle` and `KnimeFeature` in the case of KNIME engine (defined in [`knime_implementation.py`](./ontology_populator/implementations/knime/knime_implementation.py)).

<!-- To create the engine-specific instances (implementations and components) -->

## Pipeline Generator
This is the main module responsible for generating the data workflows using the Knowledge Graph from the user input (intent).

```bash
cd pipeline_generator
python3 optimized_pipeline_generator.py
```
Upon running the script, the user will be prompted to enter the information related to the intent: 
- The intent name (any name chosen by the user).
- The dataset name (one of the datasets in [`datasets`](./dataset_annotator/datasets) after running the annotation script).
- The task to be performed (an existing task).
- The algorithm to solve the task (in the case of some tasks, such as DataVisualization).
- The threshold (percentage) for the components to be used in each of the data preprocessing tasks.
- A directory where the generated workflows will be stored.
- Values for the exposed parameters of the algorithms used to solve the task (differs from one algorithm to another).

```bash
Introduce the intent name [VisualizationIntent]:
Introduce the dataset name [titanic.csv]:
Introduce the task name [DataVisualization]:
Choose a visualization algorithm from the following (< visualization algorithms >):
Choose a threshold component percentage (for the preprocessing components) (100, 75, 50, 25) (%):
Introduce the folder to save the workflows:
< Value choices for the exposed parameters of the algorithms used >:
```

## Pipeline Translator
This is the module responsible for translating the generated workflows into executable KNIME workflows. To translate a specific workflow (ttl-formatted file), the following command can be used:

```bash
cd pipeline_translator
python3 general_pipeline_translator.py --keep < source_file > < destination_folder >
```
In the destination folder, there will be a `.knwf` compressed file along with the folder containing the KNIME nodes if `--keep` is used; otherwise, only the `.knwf` file will be generated and it will need to be manually decompressed. 

## Experimental Runs
### Benchmarking the Performance
For each of the scenarios tested, there are two scripts:
- [`fake_cbox_generator.py`](./experimental_runs/new-bruteforce-runs/fake_cbox_generator.py): creates a number of CBOXes with each of them posessing different values for the following complexity parameters: (number of components, number of requirements per component and number of components per requirement). The generate CBOXes are stored in the [`fake_cboxes`](./experimental_runs/new-bruteforce-runs/fake_cboxes) folder.

```bash
cd experimental_runs
cd < new-bruteforce-runs OR mid-case-runs OR best-case-runs >
python3 fake_cbox_generator.py
```

- [`experiment_runner.py`](./experimental_runs/new-bruteforce-runs//experiment_runner.py): runs the experiments based on the generated CBOXes in the [`fake_cboxes`](./experimental_runs/new-bruteforce-runs/fake_cboxes) directory.

```bash
cd experimental_runs
cd < new-bruteforce-runs OR mid-case-runs OR best-case-runs >
python3 experiment_runner.py
```

As for the case of the previous workflow generator, the setting in the following [repository](https://github.com/dtim-upc/IntentSpecification2WorkflowGenerator/tree/main/experiment_lab) was used.

### Evaluating the Rule-based Selection
The evaluation of the rule-based selection was carried out for the workflows solving the Classification task by comparing the workflows results from the bruteforce workflow generator against the selective workflow generator by performing the following steps:
1. Generating the set of workflows from each generator for each dataset.
2. Translating all the generated workflow from each generator to KNIME workflows at once using the bash script in [`translate_workflows.sh`](./pipeline_translator/translate_workflows.sh).
3. Importing all the KNIME workflows into the KNIME engine and running each workflow individually to evaluate its result.

## Demo
The demo is a web application that enables the user to generate workflows based on the inputs discussed in this [section](#pipeline-generator). The user will eventually have the choice to import the ontology-generated workflows as they are or import the KNIME-translated versions.

To ensure the successful run of the demo, all the dependencies installed in the [requirements](#requirements) section need to be installed. Then, the following commands must be run:

- Run the backend from the root directory
```bash
cd demo/demo_api
flask --app api.py run
```

- Run the frontend from the root directory
```bash
cd demo/demo_web
npm run dev
```

The following GIF shows the demo:
![Project Demo](./demo.gif)

## Framework Extension Guidelines

### Engine-Agnostic Extension Guidelines and References

| **Concept**                  | **Description**                                                                                                                                                                                                                                                                                                            | **Reference**                                                                                                                                                                                                                                             |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Task**                     | Represents the data tasks possible to perform on a dataset. All of the tasks are defined in the CBOX of the ontology, so any extension of these tasks will be in the CBOX.                                                                                                                                            | Refer to the CBOX generator [here](./ontology_populator/cbox_generator.py).                                                                                    |
| **Algorithm**                | Represents the conceptual definition of possible solutions for each task and are directly connected to the Task instances they solve. They are also in the CBOX.                                                                                                                                                      | Refer to the CBOX generator [here](./ontology_populator/cbox_generator.py).                                                                                    |
| **Implementation**           | Represents the executable form of an algorithm. Each algorithm has at least one implementation instance that references it. Specialized subclasses like Learner Implementation and Visualizer Implementation are defined in the TBOX.                                                                                   | Refer to the Implementation class [here](./ontology_populator/implementations/core/implementation.py) and the TBOX generator [here](./ontology_populator/tbox_generator.py). |
| **Input & Output Specifications** | These classes define constraints on an implementation's inputs and outputs. Constraints are encoded as SHACL shapes, defined in the CBOX, and referenced in an implementation definition.                                                                                                                         | Refer to the shapes defined in the CBOX [here](./ontology_populator/cbox_generator.py).                                                                        |
| **Component**                | An abstraction level of the implementation concept. Each implementation has at least one component, which may use different methods. Component subclasses are defined in the TBOX.                                                                                                                                  | Refer to the definition of the implementation class [here](./ontology_populator/implementations/core/component.py) and the TBOX generator [here](./ontology_populator/tbox_generator.py). |
| **Transformation**           | A set of data annotation transformations expressed in SPARQL queries specific to each component. These are defined manually within each component instance. Includes Copy Transformation and Load Transformation classes for specific tasks.                                                                             | Refer to the Transformation classes [here](./ontology_populator/implementations/core/transformation.py).                                                       |
| **Rule**                     | Represents domain knowledge used to select components for preprocessing tasks. These are defined within preprocessing component definitions.                                                                                                                                                                             | Refer to the examples [here](./ontology_populator/implementations/knime/normalization.py).                                                                      |

### Engine-Specific Extension Guidelines and References

| **Concept**         | **Description**                                                                                                                                                                                                                                                | **Reference**                                                                                                                                                                                                                                               |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Parameter**       | Represents the algorithm and execution engine configurations. An engine-specific subclass is created to accommodate specific engine parameters needed for translation.                                                                                       | Refer to the Parameter class [here](./ontology_populator/implementations/core/parameter.py) and an example subclass [here](./ontology_populator/implementations/knime/knime_implementation.py). |
| **Implementation**  | Engine-specific subclasses include specific implementation configurations. Engine-specific implementations for a certain algorithm are defined separately.                                                                                                   | Refer to the Implementation class [here](./ontology_populator/implementations/core/implementation.py). Example engine-specific subclass [here](./ontology_populator/implementations/knime/knime_implementation.py) and SVM implementations [here](./ontology_populator/implementations/knime/svm.py). |
| **Data Annotator**  | Ensures datatype definitions are consistent between the data annotator used in the workflow generator and the targeted execution engine.                                                                                                                   | Refer to the engine-specific data annotator [here](./dataset_annotator/knime_annotator.py).                                                                      |
| **Additional Classes** | Additional classes may need to be defined depending on the specific execution engine requirements to ensure successful translation.                                                                                                                      | Examples of engine-specific classes [here](./ontology_populator/implementations/knime/knime_implementation.py).
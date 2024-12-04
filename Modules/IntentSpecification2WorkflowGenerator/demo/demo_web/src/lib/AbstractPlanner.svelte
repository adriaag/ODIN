<script lang="ts">
  import Textfield from "@smui/textfield";
  import Button, { Label } from "@smui/button";
  import CircularProgress from "@smui/circular-progress";
  import Autocomplete from "@smui-extra/autocomplete";
  import { createEventDispatcher } from "svelte";
  import Paper, { Content, Title } from "@smui/paper";
  import ParameterVisualizer from "./ParametersVisualizer/ParameterVisualizer.svelte";
  import { GetMapConfigData } from "./ParametersConfigStore";

  const dispatch = createEventDispatcher();

  let datasets: { [key: string]: string } = {};
  let problems: { [key: string]: string } = {};
  let dataset_columns: { [key: string]: string } = {};
  let viz_algorithms: { [key: string]: string } = {};

  // percentage
  let preprocessing_component_percentage = 0;
  let preprocessing_component_options = [100.0, 75.0, 50.0, 25.0];

  let intent_name = "";
  let dataset = "";
  let problem = "";
  let viz_algorithm = "";

  let loading_datasets = true;
  let loading_problems = true;
  let loading_viz_algorithms = true;
  let loading_dataset_columns = true;

  let creating_plans = false;

  fetch("http://localhost:5000/datasets")
    .then((response) => response.json())
    .then((data) => {
      datasets = data;
      loading_datasets = false;
    });

  fetch("http://localhost:5000/problems")
    .then((response) => response.json())
    .then((data) => {
      problems = data;
      loading_problems = false;
    });

  async function run_planner(): Promise<void> {
    let final_dataset = datasets[dataset];
    let final_problem = problems[problem];

    creating_plans = true;

    await fetch("http://localhost:5000/abstract_planner", {
      method: "POST",
      body: JSON.stringify({
        intent_name: intent_name,
        dataset: final_dataset,
        problem: final_problem,
        algorithm: viz_algorithm,
        preprocessing_percentage: preprocessing_component_percentage,
        exposed_parameters: GetMapConfigData(),
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    dispatch("abstract_plans");
    creating_plans = false;
  }

  fetch("http://localhost:5000/visualization_algorithms")
    .then((response) => response.json())
    .then((data) => {
      viz_algorithms = data;
      loading_viz_algorithms = false;
    });
</script>

<Paper variant="unelevated" class="flex-column">
  <Title>Abstract Planner</Title>
  <Content class="flex-column">
    {#if loading_datasets || loading_problems || creating_plans}
      <CircularProgress style="height: 32px; width: 32px;" indeterminate />
    {:else}
      <Textfield variant="outlined" bind:value={intent_name} label="Intent name"></Textfield>
      <Autocomplete
        options={Object.keys(datasets)}
        textfield$variant="outlined"
        bind:value={dataset}
        label="Dataset"
      />
      <Autocomplete
        options={preprocessing_component_options}
        textfield$variant="outlined"
        bind:value={preprocessing_component_percentage}
        label="Pre-processing component %"
      />
      <Autocomplete
        options={Object.keys(problems)}
        textfield$variant="outlined"
        bind:value={problem}
        label="Problem"
      />
      {#if problem === "DataVisualization"}
        <Autocomplete
          options={Object.keys(viz_algorithms)}
          textfield$variant="outlined"
          bind:value={viz_algorithm}
          label="Visualization Options"
        />
        {#if viz_algorithm !== ""}
          <ParameterVisualizer
            algorithm={viz_algorithms[viz_algorithm]}
            problem={problems[problem]}
            dataset={datasets[dataset]}
          />
        {/if}
      {:else if problem === "Classification"}
        <ParameterVisualizer
          algorithm={viz_algorithms[viz_algorithm]}
          problem={problems[problem]}
          dataset={datasets[dataset]}
        />
      {/if}

      <Button on:click={run_planner} variant="outlined">
        <Label>Run Abstract Planner</Label>
      </Button>
    {/if}
  </Content>
</Paper>

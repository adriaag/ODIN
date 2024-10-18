<script lang="ts">
  import Textfield from "@smui/textfield";
  import Button, { Label } from "@smui/button";
  import CircularProgress from "@smui/circular-progress";
  import Autocomplete from "@smui-extra/autocomplete";
  import { createEventDispatcher } from "svelte";
  import Paper, { Content, Title } from "@smui/paper";
  import PieChartVisualizationOptions from "./visualizationComponents/piechartvisualizationoptions.svelte";
  import BarChartVisualizationOptions from "./visualizationComponents/barchartvisualizationoptions.svelte";
  import HistogramVisualizationOptions from "./visualizationComponents/histogramchartvisualizationoptions.svelte";
  import ScatterPlotVisualizationOptions from "./visualizationComponents/scatterplotvisualizationoptions.svelte";
  import LinePlotVisualizationOptions from "./visualizationComponents/lineplotvisualizationoptions.svelte";
  import HeatmapVisualizationOptions from "./visualizationComponents/heatmapvisualizationoptions.svelte";
  

  const dispatch = createEventDispatcher();

  let datasets: { [key: string]: string } = {};
  let problems: { [key: string]: string } = {};
  let dataset_columns: { [key: string]: string } = {};
  let viz_algorithms: { [key: string]: string } = {};

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

    let viz_params = {
      categorical_column_choice: categorical_column_choice,
      numerical_column_choice: numerical_column_choice,
      group_numerical_column_choices: group_numerical_column_choices,
      x_axis_column: x_axis_column,
      y_axis_column: y_axis_column,
      y_axis_column_group: y_axis_column_group,
      x_axis_column_group: x_axis_column_group,
    };

    await fetch("http://localhost:5000/abstract_planner", {
      method: "POST",
      body: JSON.stringify({
        intent_name: intent_name,
        dataset: final_dataset,
        problem: final_problem,
        
        visualization_parameters: viz_params
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

  let categorical_column_choice: string = "";
  let numerical_column_choice: string = "";
  let x_axis_column: string = "";
  let y_axis_column: string = "";
  let y_axis_column_group: string[] = [];
  let x_axis_column_group: string[] = [];

  let group_numerical_column_choices: string[] = [];
  $: {
    let map = {
      categorical_column_choice: categorical_column_choice,
      numerical_column_choice: numerical_column_choice,
      group_numerical_column_choices: group_numerical_column_choices,
      x_axis_column: x_axis_column,
      y_axis_column: y_axis_column,
      y_axis_column_group: y_axis_column_group,
      x_axis_column_group: x_axis_column_group,
    };
    // console.log(`wassabi ${JSON.stringify(map)}`);
  }
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

        {#if viz_algorithm === "PieChart"}
          <PieChartVisualizationOptions
            bind:categorical_column_choice
            bind:numerical_column_choice
            dataset={datasets[dataset]}
          />
        {:else if viz_algorithm === "BarChart"}
          <BarChartVisualizationOptions
            bind:group_numerical_column_choices
            bind:categorical_column_choice
            dataset={datasets[dataset]}
          />
        {:else if viz_algorithm === "Histogram"}
          <HistogramVisualizationOptions
            bind:group_numerical_column_choices
            bind:numerical_column_choice
            dataset={datasets[dataset]}
          />
        {:else if viz_algorithm === "ScatterPlot"}
          <ScatterPlotVisualizationOptions
            bind:x_axis_column
            bind:y_axis_column
            dataset={datasets[dataset]}
          />
        {:else if viz_algorithm === "LinePlot"}
          <LinePlotVisualizationOptions
            bind:x_axis_column
            bind:y_axis_column_group
            dataset={datasets[dataset]}
          />
        {:else if viz_algorithm === "Heatmap"}
          <HeatmapVisualizationOptions
            bind:y_axis_column
            bind:x_axis_column_group
            dataset={datasets[dataset]}
          />
        {/if}
      {/if}

      <Button on:click={run_planner} variant="outlined">
        <Label>Run Abstract Planner</Label>
      </Button>
    {/if}
  </Content>
</Paper>

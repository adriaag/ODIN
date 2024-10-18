<script lang="ts">
    import Autocomplete from "@smui-extra/autocomplete";
    import { fetchColumns } from "./CommonReqs";
    let dataset_columns: { [key: string]: string } = {};
    export let x_axis_column: string = "";
    export let y_axis_column : string = "";
    export let dataset: string;
  
    async function loadData(){
        dataset_columns = await fetchColumns(dataset);
    }
  
  </script>
  
  {#await loadData()}
    <p>loading components</p>
  {:then value}
    <Autocomplete
      options={Object.keys(dataset_columns)}
      textfield$variant="outlined"
      bind:value={x_axis_column}
      label="Pick a column on x-axis"
    />
  
    <Autocomplete
    options={Object.keys(dataset_columns)}
    textfield$variant="outlined"
    bind:value={y_axis_column}
    label="Pick a column on y-axis"
  />
  {/await}
  
<script lang="ts">
    import Autocomplete from "@smui-extra/autocomplete";
    import { fetchCategoricalColumns, fetchNumericalColumns } from "./CommonReqs";
    export let categorical_column_choice: string = "";
    export let numerical_column_choice : string = "";
    let dataset_categorical_columns: { [key: string]: string } = {};
    let dataset_numerical_columns: { [key: string]: string } = {};
  
  
    export let dataset: string;
  
    async function loadData(){
      const [categoricalData, numericalData] = await Promise.all([
          fetchCategoricalColumns(dataset),
          fetchNumericalColumns(dataset),
        ]);
        dataset_categorical_columns = categoricalData;
        dataset_numerical_columns = numericalData;
    }
  
  </script>
  
  {#await loadData()}
    <p>loading components</p>
  {:then value}
    <Autocomplete
      options={Object.keys(dataset_categorical_columns)}
      textfield$variant="outlined"
      bind:value={categorical_column_choice}
      label="Categorical Column Choice"
    />
  
    <Autocomplete
    options={Object.keys(dataset_numerical_columns)}
    textfield$variant="outlined"
    bind:value={numerical_column_choice}
    label="Numerical Column Choice"
  />
  {/await}
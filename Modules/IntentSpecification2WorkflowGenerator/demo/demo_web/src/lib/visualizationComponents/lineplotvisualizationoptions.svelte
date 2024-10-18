<script lang="ts">
    import { fetchColumns } from "./CommonReqs";
    import Autocomplete from "@smui-extra/autocomplete";
    import Checkbox from "@smui/checkbox";
    import FormField from "@smui/form-field";

    let dataset_columns: { [key: string]: string } = {};
    export let x_axis_column: string = "";
    export let y_axis_column_group : string[] = [];
    export let dataset: string;
  
    async function loadData(){
        dataset_columns = await fetchColumns(dataset);
    }

  
    $:{
        if (x_axis_column) {
            y_axis_column_group = []
        }
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
    <p>Select all columns on the Y axis:</p>
    <div>
        {#each Object.keys(dataset_columns) as option}
        {#if option !== x_axis_column}
        <FormField>
            <p>{option}</p>
            <Checkbox bind:group={y_axis_column_group} value={option} />
      </FormField>
      {/if}
      {/each}
  </div>
  {/await}
  
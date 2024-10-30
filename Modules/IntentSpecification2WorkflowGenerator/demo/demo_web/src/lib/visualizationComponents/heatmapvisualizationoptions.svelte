<script lang="ts">
    import { fetchColumns } from "./CommonReqs";
    import Autocomplete from "@smui-extra/autocomplete";
    import Checkbox from "@smui/checkbox";
    import FormField from "@smui/form-field";

    let dataset_columns: { [key: string]: string } = {};
    export let y_axis_column : string = "";
    export let x_axis_column_group: string[] = [];
    export let dataset: string;
  
    async function loadData(){
        dataset_columns = await fetchColumns(dataset);
        console.log(`wasaabi, ${dataset_columns}`)
    }
  
    $:{
        if (y_axis_column) {
            x_axis_column_group = []
        }
    }
  </script>
  
  {#await loadData()}
    <p>loading components</p>
  {:then value}
    <Autocomplete
      options={Object.keys(dataset_columns)}
      textfield$variant="outlined"
      bind:value={y_axis_column}
      label="Pick a column on y-axis"
    />
    <p>Select all columns on the X axis:</p>
    <div>
        {#each Object.keys(dataset_columns) as option}
        {#if option !== y_axis_column}
        <FormField>
            <p>{option}</p>
            <Checkbox bind:group={x_axis_column_group} value={option} />
      </FormField>
      {/if}
      {/each}
  </div>
  {/await}
  
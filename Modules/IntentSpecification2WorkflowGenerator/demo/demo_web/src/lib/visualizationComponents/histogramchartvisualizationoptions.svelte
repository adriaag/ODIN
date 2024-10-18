<script lang="ts">
    import Autocomplete from "@smui-extra/autocomplete";
    import { fetchCategoricalColumns, fetchNumericalColumns } from "./CommonReqs";
    import Checkbox from "@smui/checkbox";
    import FormField from "@smui/form-field";
  
    let dataset_numerical_columns: { [key: string]: string } = {};
  
    let include_frequency_columns = false;
  
    export let dataset: string;
    export let numerical_column_choice: string = "";
    export let group_numerical_column_choices: string[] = [];
  
    async function loadData() {
        dataset_numerical_columns = await fetchNumericalColumns(dataset);
    }

    $:{
        if (numerical_column_choice) {
            group_numerical_column_choices = []
        }
    }
  </script>
  
  {#await loadData()}
    <p>data is loading.</p>
  {:then value}
    <Autocomplete
      options={Object.keys(dataset_numerical_columns)}
      textfield$variant="outlined"
      bind:value={numerical_column_choice}
      label="Numerical Column Choice"
    />
  
    <div>
      <FormField>
        <p>Include frequency columns?</p>
        <Checkbox bind:checked={include_frequency_columns} />
      </FormField>
    </div>
    <div >
      {#if include_frequency_columns}
      <div>
          {#each Object.keys(dataset_numerical_columns) as option}
          {#if option !== numerical_column_choice}
          
          <FormField>
              <p>{option}</p>
              <Checkbox bind:group={group_numerical_column_choices} value={option} />
        </FormField>
        {/if}
        {/each}
    </div>
    {/if}
  </div>
  {/await}
  
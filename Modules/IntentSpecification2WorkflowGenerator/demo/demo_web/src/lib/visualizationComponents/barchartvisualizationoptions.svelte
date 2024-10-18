<script lang="ts">
  import Autocomplete from "@smui-extra/autocomplete";
  import { fetchCategoricalColumns, fetchNumericalColumns } from "./CommonReqs";
  import Checkbox from "@smui/checkbox";
  import FormField from "@smui/form-field";

  let dataset_categorical_columns: { [key: string]: string } = {};
  let dataset_numerical_columns: { [key: string]: string } = {};

  let include_frequency_columns = false;
  let number_of_frequency: number = 1;

  export let dataset: string;
  export let categorical_column_choice: string = "";
  export let group_numerical_column_choices: string[] = [];

  async function loadData() {
    const [categoricalData, numericalData] = await Promise.all([
      fetchCategoricalColumns(dataset),
      fetchNumericalColumns(dataset),
    ]);
    dataset_categorical_columns = categoricalData;
    dataset_numerical_columns = numericalData;
  }
</script>

{#await loadData()}
  <p>data is loading.</p>
{:then value}
  <Autocomplete
    options={Object.keys(dataset_categorical_columns)}
    textfield$variant="outlined"
    bind:value={categorical_column_choice}
    label="Categorical Column Choice"
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
        <FormField>
            <p>{option}</p>
            <Checkbox bind:group={group_numerical_column_choices} value={option} />
      </FormField>
      {/each}
  </div>
  {/if}
</div>
{/await}

<script lang="ts">
  import {
    fetchCategoricalColumns,
    fetchColumns,
    fetchNumericalColumns,
  } from "../visualizationComponents/CommonReqs";
  import Autocomplete from "@smui-extra/autocomplete";
  import { map } from "../ParametersConfigStore";
  import FormField from "@smui/form-field";
  import Checkbox from "@smui/checkbox";

  export let uriRef: string;
  export let valueType: string;
  export let slug: string;
  export let condition: string;
  export let dataset: string;
  let hasCondition = condition !== "";
  let conditionToggle = !hasCondition;

  enum ValueTypeEnum {
    CATEGORICAL = "CATEGORICAL",
    INCLUDED = "INCLUDED",
    NUMERICAL = "NUMERICAL",
    COLUMN = "COLUMN",
    COMPLETE = "COMPLETE",
  }

  function GetValueType(vType: String, condition: string) {
    let configDict: Record<string, boolean> = {};
    configDict[ValueTypeEnum.CATEGORICAL] = vType.includes("CATEGORICAL");
    configDict[ValueTypeEnum.INCLUDED] = condition.includes("INCLUDED");
    configDict[ValueTypeEnum.NUMERICAL] = vType.includes("NUMERICAL");
    configDict[ValueTypeEnum.COLUMN] = vType.includes("COLUMN");
    configDict[ValueTypeEnum.COMPLETE] = vType.includes("COMPLETE");
    console.log(configDict);
    return configDict;
  }

  let dataset_categorical_columns: { [key: string]: string } = {};
  let dataset_numerical_columns: { [key: string]: string } = {};
  let dataset_columns: { [key: string]: string } = {};

  let valueTypeEnum: Record<string, boolean> = {};
  async function loadData() {
    valueTypeEnum = GetValueType(valueType, condition);
    if (valueTypeEnum[ValueTypeEnum.CATEGORICAL]) {
      dataset_categorical_columns = await fetchCategoricalColumns(dataset);
    } else if (valueTypeEnum[ValueTypeEnum.NUMERICAL]) {
      dataset_numerical_columns = await fetchNumericalColumns(dataset);
    } else if (valueTypeEnum[ValueTypeEnum.COLUMN] || valueTypeEnum[ValueTypeEnum.COMPLETE]) {
      dataset_columns = await fetchColumns(dataset);

      if (valueTypeEnum[ValueTypeEnum.COMPLETE]) {
        dataset_columns["<RowID>"] = "";
      }
    }
  }

  let categoricalColumnChoice: { uriRef: string; value: string } = { uriRef: uriRef, value: "" };
  $: console.log($map);

  function setUriRefParam(key: number) {
    switch (key) {
      case 1:
        let uri = $map.categorical_column_choice.find((x) => x.uriRef === uriRef);
        if (uri == undefined) {
          $map.categorical_column_choice.push(categoricalColumnChoice);
        } else {
          categoricalColumnChoice = uri;
        }
        break;
      case 2:
        $map.numerical_column_choice.uriRef = uriRef;
        break;
      case 3:
        $map.y_axis_column_group.uriRef = uriRef;
        break;
      case 4:
        $map.y_axis_column.uriRef = uriRef;
        break;
      case 5:
        $map.x_axis_column_group.uriRef = uriRef;
        break;
      case 6:
        $map.x_axis_column.uriRef = uriRef;
        break;
      case 7:
        $map.group_numerical_column_choices.uriRef = uriRef;
        break;
      case 8:
        $map.y_axis_column_group.uriRef = uriRef;
        break;
      default:
        break;
    }
    return "";
  }
</script>

{#await loadData()}
  <p>loading components</p>
{:then value}
  {#if hasCondition}
    <FormField>
      <p>Has {slug}?</p>
      <Checkbox bind:checked={conditionToggle} />
    </FormField>
  {/if}

  {#if (hasCondition && conditionToggle) || !hasCondition}
    {#if valueTypeEnum[ValueTypeEnum.CATEGORICAL] && !valueTypeEnum[ValueTypeEnum.INCLUDED]}
      {setUriRefParam(1)}

      {#each $map.categorical_column_choice as choice}
        {#if choice.uriRef == uriRef}
          <Autocomplete
            options={Object.keys(dataset_categorical_columns)}
            textfield$variant="outlined"
            label={slug}
            bind:value={choice.value}
          />
        {/if}
      {/each}
    {:else if valueTypeEnum[ValueTypeEnum.NUMERICAL] && !valueTypeEnum[ValueTypeEnum.INCLUDED]}
      {setUriRefParam(2)}
      <Autocomplete
        options={Object.keys(dataset_numerical_columns)}
        textfield$variant="outlined"
        bind:value={$map.numerical_column_choice.value}
        label={slug}
      />
    {:else if valueTypeEnum[ValueTypeEnum.COLUMN] || valueTypeEnum[ValueTypeEnum.COMPLETE]}
      {#if slug.includes(" Y ")}
        {#if valueTypeEnum[ValueTypeEnum.INCLUDED]}
          {setUriRefParam(3)}

          {#each Object.keys(dataset_columns) as option}
            {#if option !== $map.x_axis_column.value}
              <FormField>
                <p>{option}</p>
                <Checkbox bind:group={$map.y_axis_column_group.value} value={option} />
              </FormField>
            {/if}
          {/each}
        {:else}
          {setUriRefParam(4)}
          <Autocomplete
            options={Object.keys(dataset_columns)}
            textfield$variant="outlined"
            bind:value={$map.y_axis_column.value}
            label={slug}
          />
        {/if}
      {:else if valueTypeEnum[ValueTypeEnum.INCLUDED]}
        {setUriRefParam(5)}

        {#each Object.keys(dataset_columns) as option}
          {#if option !== $map.y_axis_column.value}
            <FormField>
              <p>{option}</p>
              <Checkbox bind:group={$map.x_axis_column_group.value} value={option} />
            </FormField>
          {/if}
        {/each}
      {:else}
        {setUriRefParam(6)}

        <Autocomplete
          options={Object.keys(dataset_columns)}
          textfield$variant="outlined"
          bind:value={$map.x_axis_column.value}
          label={slug}
        />
      {/if}
    {:else if valueTypeEnum[ValueTypeEnum.INCLUDED] && valueTypeEnum[ValueTypeEnum.NUMERICAL]}
      {setUriRefParam(7)}

      <div>
        {#each Object.keys(dataset_numerical_columns) as option}
          {#if option !== $map.numerical_column_choice.value}
            <FormField>
              <p>{option}</p>
              <Checkbox bind:group={$map.group_numerical_column_choices.value} value={option} />
            </FormField>
          {/if}
        {/each}
      </div>
    {:else if valueTypeEnum[ValueTypeEnum.INCLUDED] && valueTypeEnum[ValueTypeEnum.CATEGORICAL]}
      {setUriRefParam(3)}
      <div>
        {#each Object.keys(dataset_columns) as option}
          {#if option !== $map.x_axis_column.value}
            <FormField>
              <p>{option}</p>
              <Checkbox bind:group={$map.y_axis_column_group.value} value={option} />
            </FormField>
          {/if}
        {/each}
      </div>
    {/if}
  {/if}
{/await}

<script lang="ts">
  import { GetExposedParams, type PieChartData } from "../visualizationComponents/CommonReqs";
  import ParameterComponentBuilder from "./ParameterComponentBuilder.svelte";

  export let problem: string;
  export let algorithm: string;
  export let dataset: string;

  let exposedParams: { uriRef: string; slug: string; valueType: string; condition: string }[];

  async function loadParameters() {
    let temp = await GetExposedParams(problem, algorithm);
    exposedParams = [];
    temp.forEach((element) => {
      for (const key in element) {
        exposedParams.push({
          uriRef: key,
          slug: element[key][0],
          valueType: element[key][1],
          condition: element[key][2],
        });
      }
    });
    console.log(exposedParams);
  }
</script>

{#await loadParameters()}
  <p>buildingComponents</p>
{:then value}
  {#each exposedParams as param}
    <ParameterComponentBuilder
      uriRef={param.uriRef}
      slug={param.slug}
      valueType={param.valueType}
      condition={param.condition}
      {dataset}
    />
  {/each}
{/await}

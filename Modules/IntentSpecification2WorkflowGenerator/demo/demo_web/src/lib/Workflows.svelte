<script lang="ts">
    import Button from "@smui/button";
    import Paper, {Content, Subtitle, Title} from '@smui/paper';
    import Accordion, {Content as AccContent, Header, Panel} from '@smui-extra/accordion';
    import List, {Item, Label, Meta} from '@smui/list';
    import IconButton, { Icon } from '@smui/icon-button';
    import CircularProgress from "@smui/circular-progress";
    import Tooltip, {Wrapper} from '@smui/tooltip';
    import {removeLastPart, windowsStyleSort} from "./utils";

    let plans: string[];
    let groups: { [key: string]: string[] };
    let groups_opened: { [key: string]: boolean }

    let loading = true;

    async function initialize() {
        let response = await fetch('http://localhost:5000/workflow_plans');
        plans = await response.json();
        groups = {};
        groups_opened = {};

        for (let key of plans) {
            groups_opened[key] = false;
            let group = removeLastPart(key);
            if (!groups.hasOwnProperty(group)) {
                groups[group] = [];
            }
            groups[group].push(key);
        }
        loading = false;
    }

    initialize();

    async function download_rdf(plan_id: string) {
        let element = document.createElement('a');
        element.setAttribute('href', 'http://localhost:5000/workflow_plans/rdf/' + plan_id);
        element.setAttribute('download', 'rdf_plans.zip');
        element.click();
    }

    async function download_all_rdf() {
        let element = document.createElement('a');
        element.setAttribute('href', 'http://localhost:5000/workflow_plans/rdf/all');
        element.setAttribute('download', 'rdf_plans.zip');
        element.click();
    }

    function download_knime(plan_id: string) {
        let element = document.createElement('a');
        element.setAttribute('href', 'http://localhost:5000/workflow_plans/knime/' + plan_id);
        element.setAttribute('download', 'rdf_plans.zip');
        element.click();
    }

    function download_all_knime() {
        let element = document.createElement('a');
        element.setAttribute('href', 'http://localhost:5000/workflow_plans/knime/all');
        element.setAttribute('download', 'rdf_plans.zip');
        element.click();
    }

</script>

<Paper variant="unelevated" class="flex-column overflow-80">
    <Title>Final Workflows</Title>
    {#if loading}
        <CircularProgress style="height: 32px; width: 32px;" indeterminate/>
    {:else}
        <Content class="flex-column overflow-50">
            <div class="overflow-50">
                <Accordion>
                    {#each Object.keys(groups) as group_id}
                        <Panel bind:open={groups_opened[group_id]}>
                            <Header>
                                {group_id}
                                <IconButton slot="icon" toggle pressed={groups_opened[group_id]} ripple={false}>
                                    <Icon class="material-icons" on>expand_less</Icon>
                                    <Icon class="material-icons">expand_more</Icon>
                                </IconButton>
                            </Header>
                            <AccContent>
                                <List>
                                    {#each windowsStyleSort(groups[group_id]) as element}
                                        <div class="item-div">
                                            <Item>
                                                <div class="inner-item-div">
                                                    <Label>{element}</Label>
                                                </div>
                                                <Meta>
                                                    <Wrapper>
                                                        <IconButton class="material-icons"
                                                                    on:click={() => download_rdf(element)}>share
                                                        </IconButton>
                                                        <Tooltip>Download RDF representation</Tooltip>
                                                    </Wrapper>
                                                    <Wrapper>
                                                        <IconButton class="material-icons"
                                                                    on:click={() => download_knime(element)}>download
                                                        </IconButton>
                                                        <Tooltip>Download KNIME representation</Tooltip>
                                                    </Wrapper>
                                                </Meta>
                                            </Item>
                                        </div>
                                    {/each}
                                </List>
                            </AccContent>
                        </Panel>
                    {/each}
                </Accordion>
            </div>

            <div>
                <Button on:click={download_all_rdf} variant="outlined">
                    <Label>Download all RDF representations</Label>
                </Button>
                <Button on:click={download_all_knime} variant="outlined">
                    <Label>Download all KNIME representations</Label>
                </Button>
            </div>
        </Content>
    {/if}

</Paper>

<style>
    .inner-item-div {
        display: flex;
        justify-content: left;
        align-items: center;
    }
</style>
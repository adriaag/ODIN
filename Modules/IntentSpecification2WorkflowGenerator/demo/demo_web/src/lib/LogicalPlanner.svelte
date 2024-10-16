<script lang="ts">
    import List, {Item, Label, Meta} from '@smui/list';
    import Checkbox from '@smui/checkbox';
    import IconButton from '@smui/icon-button';
    import Button from "@smui/button";
    import Paper, {Content, Subtitle, Title} from '@smui/paper';
    import {createEventDispatcher} from 'svelte';
    import CircularProgress from '@smui/circular-progress';

    const dispatch = createEventDispatcher();

    let plans: { [key: string]: { [key: string]: string[] } };
    let keys: string[];
    let selected: string[];

    let loading = true;

    async function initialize() {
        let response = await fetch('http://localhost:5000/abstract_plans');
        plans = await response.json();
        keys = Object.keys(plans);
        selected = Object.keys(plans || {});
        loading = false;
    }

    initialize()

    function viewAbstractPlan(plan_id: string) {
        let plan = plans[plan_id];
        dispatch('visualize_plan', {plan: plan, plan_id: plan_id});
    }

    async function run_planner() {
        loading = true;

        await fetch('http://localhost:5000/logical_planner', {
            method: 'POST',
            body: JSON.stringify(selected),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        dispatch('logical_plans');
        loading = false;
    }

</script>

<Paper variant="unelevated" class="flex-column overflow-80">
    <Title>Logical Planner</Title>
    {#if loading}
        <CircularProgress style="height: 32px; width: 32px;" indeterminate/>
    {:else}
        <Subtitle>Select the Abstract Plans to send to the Logical Planner:</Subtitle>
        <Content class="flex-column">
            <List class="overflow-30" checkList>
                {#each keys as key}
                    <div class="item-div">
                        <Item>
                            <div class="inner-item-div">
                                <Meta>
                                    <Checkbox bind:group={selected} value="{key}"/>
                                </Meta>
                                <Label>{key.split('#').at(-1)}</Label>
                            </div>
                            <Meta>
                                <IconButton class="material-icons" on:click={() => viewAbstractPlan(key)}>visibility
                                </IconButton>
                            </Meta>
                        </Item>
                    </div>
                {/each}
            </List>

            <Button on:click={run_planner} variant="outlined">
                <Label>Run Logical Planner</Label>
            </Button>
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
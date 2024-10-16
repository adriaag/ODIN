<script lang="ts">
    import Card from "@smui/card";
    import AbstractPlanner from "./lib/AbstractPlanner.svelte";
    import Tab, {Icon, Label} from '@smui/tab';
    import TabBar from '@smui/tab-bar';
    import LogicalPlanner from "./lib/LogicalPlanner.svelte";
    import WorkflowPlanner from "./lib/WorkflowPlanner.svelte";
    import Workflows from "./lib/Workflows.svelte";
    import AbstractPlanVisualizer from "./lib/AbstractPlanVisualizer.svelte";

    let tabs = [
        {
            icon: 'start',
            label: 'Abstract Planner',
        },
        {
            icon: 'call_split',
            label: 'Logical Planner',
        },
        {
            icon: 'settings',
            label: 'Workflow Planner',
        },
        {
            icon: 'share',
            label: 'Workflows',
        },
        {
            icon: 'visibility',
            label: 'Visualizer',
        },
    ];

    let active = tabs[0];


    function abstract_planner_finished() {
        active = tabs[1];
    }

    function logical_planner_finished() {
        active = tabs[2];
    }

    function workflow_planner_finished() {
        active = tabs[3];
    }

    let view_plan_id: string;
    let view_plan: { [key: string]: string[] };

    function visualize_plan(event: any) {
        view_plan_id = event.detail.plan_id;
        view_plan = event.detail.plan;

        active = tabs[4];
    }

</script>

<main>
    <link
            rel="stylesheet"
            href="node_modules/svelte-material-ui/themes/svelte.css"
            media="(prefers-color-scheme: light)"
    />
    <!-- Hint where we get fonts from. -->
    <link rel="preconnect" href="https://fonts.googleapis.com"/>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>

    <!-- Material Icons, Roboto, and Roboto Mono fonts -->
    <link
            href="https://fonts.googleapis.com/css2?family=Material+Icons&Roboto+Mono:ital@0;1&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"
            rel="stylesheet"
    />

    <div class="center">
        <Card padded class="main-card">
            <TabBar {tabs} let:tab bind:active>
                <Tab {tab}>
                    <Icon class="material-icons">{tab.icon}</Icon>
                    <Label>{tab.label}</Label>
                </Tab>
            </TabBar>
            <div class:hide={active.label !== 'Abstract Planner'}>
                <AbstractPlanner on:abstract_plans={abstract_planner_finished}></AbstractPlanner>
            </div>
            {#if active.label === 'Logical Planner'}
                <LogicalPlanner on:logical_plans={logical_planner_finished}
                                on:visualize_plan={visualize_plan}></LogicalPlanner>
            {/if}
            {#if active.label === 'Workflow Planner'}
                <WorkflowPlanner on:workflow_plans={workflow_planner_finished}
                                 on:visualize_plan={visualize_plan}></WorkflowPlanner>
            {/if}
            {#if active.label === 'Workflows'}
                <Workflows></Workflows>
            {/if}
            {#if active.label === 'Visualizer'}
                <AbstractPlanVisualizer plan={view_plan} plan_id={view_plan_id}></AbstractPlanVisualizer>
            {/if}
        </Card>
    </div>

</main>

<style>
    .center {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 90vh;
    }

    .hide {
        display: none !important;
    }
</style>
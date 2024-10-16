<script lang="ts">
    import {Background, Node, Svelvet} from 'svelvet';
    import {plan_layout} from './utils'
    import CircularProgress from "@smui/circular-progress";
    import Paper, {Title} from '@smui/paper';
    import CustomEdge from "./CustomEdge.svelte";


    export let plan: { [key: string]: string[] };
    export let plan_id: string;

    let nodes: any[];
    let edges: any[];

    async function initialize() {
        let layout = await plan_layout(plan);
        nodes = layout.nodes;
        for (let node of nodes) {
            node.incoming = [];
            node.outgoing = [];
        }
        edges = layout.edges;
        for (let edge of edges) {
            let s = edge.source.split('#').at(-1)!;
            let t = edge.target.split('#').at(-1)!;
            nodes.find(n => n.id == edge.source).outgoing.push(t);
            nodes.find(n => n.id == edge.target).incoming.push(s);
        }
    }

    let initializing: Promise<void>;

    if (plan && plan_id) {
        initializing = initialize()
    }
</script>

<div class="overflow-80">
    {#if plan && plan_id}
        <Paper variant="unelevated" class="flex-column">
            <Title>{plan_id.split('#').at(-1)}</Title>
        </Paper>
        {#await initializing}
            <CircularProgress style="height: 32px; width: 32px;" indeterminate/>
        {:then _}
            <div id="canvas-div">
                <Svelvet controls edge={CustomEdge}>
                    {#each nodes as node}
                        <Node id={node.node_id} label={node.data.label} position={{x: node.x, y:node.y}}
                              dimensions={{width: node.width, height: node.height}}
                              connections={node.outgoing}>
                        </Node>
                    {/each}
                    <Background dotColor="transparent" slot="background"/>
                </Svelvet>
            </div>
        {/await}
    {:else}
        <Paper variant="unelevated" class="flex-column">
            <Title>No workflow is selected</Title>
        </Paper>
    {/if}
</div>

<style>
    #canvas-div {
        height: 60vh;
    }
</style>
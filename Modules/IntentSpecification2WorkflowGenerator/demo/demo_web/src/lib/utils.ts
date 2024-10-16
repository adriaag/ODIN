import ELK from 'elkjs/lib/elk.bundled.js'

const elk = new ELK({
    defaultLayoutOptions: {
        'elk.algorithm': 'layered',
        'org.eclipse.elk.spacing.nodeNode': '60',
        'elk.layered.spacing.nodeNodeBetweenLayers': '100',
        'org.eclipse.elk.layered.spacing.edgeNodeBetweenLayers': '50.0',
        'org.eclipse.elk.spacing.edgeNode': '50.0',
    }
})

export {plan_layout, removeLastPart, windowsStyleSort};

function toTitleCase(str: string): string {
    return str.replace(
        /\w\S*/g,
        function (txt) {
            return txt.charAt(0).toUpperCase() + txt.substring(1);
        }
    );
}

function removeLastPart(inputString: string): string {
    const parts = inputString.split(' ');

    if (parts.length > 1) {
        parts.pop(); // Remove the last part
        return parts.join(' ');
    } else {
        return inputString; // Return the original string if there's only one part
    }
}

function windowsStyleSort(strings: string[]): string[] {
    return strings.slice().sort((a, b) => {
        return a.localeCompare(b, undefined, {numeric: true, sensitivity: 'base'});
    });
}

async function plan_layout(plan: { [key: string]: string[] }) {
    let nodes = Object.keys(plan).map(node => {
        let node_id = node.split('#').at(-1)!;
        let label = toTitleCase(node_id.replaceAll('_', ' ').replaceAll('-', ' ').replace('component ', ''));
        let width = 200;
        let label_width = label.length * 12;
        let height = label_width > width ? 30 * label_width / width : 30;
        return {
            id: node,
            node_id: node_id,
            data: {
                label: label,
            },
            width: width,
            height: height,
            sourcePosition: 'right',
            targetPosition: 'left',
        }
    });

    let edges = [];
    let i = 0;
    for (let source of Object.keys(plan)) {
        for (let target of plan[source]) {
            edges.push({
                id: 'e' + i,
                sources: [source],
                targets: [target],
                source: source,
                target: target,
                arrow: true,
            });
            i++;
        }
    }

    const graph = {
        id: "root",
        children: nodes,
        edges: edges
    }
    const layout = await elk.layout(graph);

    return {
        nodes: layout.children!,
        edges: layout.edges || [],
    }

}
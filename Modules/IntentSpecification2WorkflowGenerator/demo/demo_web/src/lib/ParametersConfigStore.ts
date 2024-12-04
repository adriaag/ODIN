import { writable } from 'svelte/store';

export interface ConfigMapData {
    categorical_column_choice: { uriRef: string, value: string }[],
    numerical_column_choice: {
        uriRef: string,
        value: string
    },
    group_numerical_column_choices: {
        uriRef: string
        value: string[]
    },
    x_axis_column: {
        uriRef: string,
        value: string
    },
    y_axis_column: {
        uriRef: string,
        value: string
    },
    y_axis_column_group: {
        uriRef: string
        value: string[]
    },
    x_axis_column_group: {
        uriRef: string
        value: string[]
    }
}

export const map = writable<ConfigMapData>({
    categorical_column_choice: [],
    numerical_column_choice: { uriRef: "", value: "" },
    group_numerical_column_choices: { uriRef: "", value: [] },
    x_axis_column: { uriRef: "", value: "" },
    y_axis_column: { uriRef: "", value: "" },
    y_axis_column_group: { uriRef: "", value: [] },
    x_axis_column_group: { uriRef: "", value: [] },
});

interface ConfigKeyVal {
    [key: string]: string | string[];
}

export function GetMapConfigData() {
    let result: ConfigKeyVal[] = [];

    const unsub = map.subscribe(newVal => {
        let values = Object.values(newVal)
        for (let i = 0; i < values.length; i++) {
            const element = values[i];
            if (Array.isArray(element)) {
                element.forEach(x => result.push({ [x.uriRef]: x.value }))
            } else if (element.uriRef !== "") {
                result.push({ [element.uriRef]: element.value })
            }
        }
        // let values: { uriRef: string, value: string | string[] }[] = Object.values(newVal)
        //     .filter(element => element.uriRef !== "" &&
        //         (Array.isArray(element.value) ? element.value.length > 0 : element.value !== ""));

        // for (let i = 0; i < values.length; i++) {
        //     const element = values[i];
        //     result.push({ [element.uriRef]: element.value })
        //     console.log("pushed " + element.uriRef)
        // }
    });
    unsub()
    return result;
}


// export const map = writable<Map<string, string | string[]>>();

let last_numerical_column_choice = "";
let last_x_col = "";
let last_y_col = "";
map.subscribe((newVal) => {
    if (newVal.numerical_column_choice.value != last_numerical_column_choice) {
        newVal.group_numerical_column_choices.value = [];
        map.set(newVal);
        last_numerical_column_choice = newVal.numerical_column_choice.value;
    }

    if (newVal.x_axis_column.value != last_x_col) {
        newVal.y_axis_column_group.value = [];
        map.set(newVal)
        last_x_col = newVal.x_axis_column.value;
    }

    if (newVal.y_axis_column.value != last_y_col) {
        newVal.x_axis_column_group.value = [];
        map.set(newVal)
        last_y_col = newVal.y_axis_column.value;
    }
})
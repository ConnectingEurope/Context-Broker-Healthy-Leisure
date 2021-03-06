import { TreeNode } from 'primeng/api/treenode';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class TreeNodeService {

    public getAllSelected(layers: TreeNode[]): TreeNode[] {
        let concatenatedLayers: TreeNode[] = layers || [];
        concatenatedLayers = concatenatedLayers.filter(t => t.selectable !== false);
        if (layers) {
            layers.forEach(t => concatenatedLayers = concatenatedLayers.concat(this.getAllSelected(t.children)));
        }
        return concatenatedLayers;
    }

}

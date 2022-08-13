let relativePath = false;

window.addEventListener('load', () => {
    displayTree(DATA);
    document.getElementById('collapse-all').addEventListener('click', handleCollapseAll);
    document.getElementById('expand-all').addEventListener('click', handleExpandAll);
    document.getElementById('relative-path').addEventListener('click', handleRelativePath);
});

function destroyTree(root = 'root') {
    document.getElementById(root).innerHTML = '';
}

function displayTree(data, root = null, indent = 0, parentId) {
    if (!root) {
        root = data.root;
    }

    if (!(root in data)) return;

    node = data[root];

    addNodeToDOM(parentId, node);

    for (const child of node.children) {
        displayTree(data, child, indent + 1, root);
    }
}

function addNodeToDOM(parentId, node) {
    const newElement = document.createElement('div');
    newElement.id = node.path;
    newElement.innerText = renderNode(node);
    newElement.classList.add('node');

    if (node.type === 'DIR') {
        newElement.classList.add('collapsible');
    }

    newElement.addEventListener('click', e => handleCollapseItem(e, node));

    document.getElementById(parentId ?? 'root').appendChild(newElement);
}

function renderNode(node) {
    if (relativePath) {
        return `${node.path.split(DATA.root)[1]} - [${node.lines}]`;
    }
    return `${node.path} - [${node.lines}]`;
}

function reRenderAllNodes() {
    debugger;
    const rootItem = document.getElementById('root').firstElementChild;
    reRenderChildNodes(rootItem);
}

function reRenderChildNodes(element) {
    element.firstChild.nodeValue = renderNode(DATA[element.id]);

    for (const child of element.children) {
        reRenderChildNodes(child);
    }
}

function handleCollapseItem(e) {
    e.stopPropagation();
    e.preventDefault();
    toggleCollapseItem(e.target);
}

function toggleCollapseItem(element) {
    const node = DATA[element.id];
    if (node.type === 'FILE') return;

    const collapsed = element.classList.contains('collapsed');
    element.classList.toggle('collapsed');

    for (const child of element.children) {
        collapsed ? child.classList.remove('hidden') : child.classList.add('hidden');
    }
}

function handleCollapseAll(e) {
    const rootItem = document.getElementById('root').firstElementChild;
    collapseAllChildren(rootItem);
}

function collapseAllChildren(element) {
    if (DATA[element.id].type === 'FILE') return;
    element.classList.add('collapsed');
    for (const child of element.children) {
        child.classList.add('hidden');
        collapseAllChildren(child);
    }
}

function handleExpandAll(e) {
    const rootItem = document.getElementById('root').firstElementChild;
    expandAllChildren(rootItem);
}

function expandAllChildren() {
    const rootItem = document.getElementById('root').firstElementChild;
    expandAllChildren(rootItem);
}

function expandAllChildren(element) {
    element.classList.remove('collapsed');
    for (const child of element.children) {
        child.classList.remove('hidden');
        expandAllChildren(child);
    }
}

function handleRelativePath(e) {
    relativePath = !relativePath;
    e.target.innerText = relativePath ? 'Absolute Path' : 'Relative Path';
    reRenderAllNodes();
}

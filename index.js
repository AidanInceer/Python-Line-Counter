window.addEventListener('load', () => {
    displayTree(DATA);
});

function displayTree(data, root = null, indent = 0, parentId) {
    if (!root) {
        root = data.root;
    }

    if (!(root in data)) return;

    node = data[root];

    // console.log(`${'  '.repeat(indent) + '| '}${node.lines} - ${node.path}`);
    addNodeToDOM(parentId, node);

    for (const child of node.children) {
        displayTree(data, child, indent + 1, root);
    }
}

function addNodeToDOM(parentId, node) {
    const newElement = document.createElement('div');
    newElement.id = node.path;
    newElement.innerText = `${node.lines} - ${node.path}`;
    newElement.classList.add('node');
    if (node.type === 'DIR') {
        newElement.classList.add('collapsable');
    }

    newElement.addEventListener('click', e => {
        e.stopPropagation();
        e.preventDefault();
        if (node.type === 'FILE') return;
        const target = e.target;
        const collapsed = target.classList.contains('collapsed');
        target.classList.toggle('collapsed');
        console.log(target.children);

        for (const child of target.children) {
            console.log(child);
            if (collapsed) {
                child.classList.remove('hidden');
            } else {
                child.classList.add('hidden');
            }
        }
    });

    document.getElementById(parentId ?? 'root').appendChild(newElement);
}

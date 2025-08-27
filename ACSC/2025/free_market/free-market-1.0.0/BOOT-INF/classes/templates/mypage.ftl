<#include "common/header.ftl">
<body class="bg-light">
<div class="container">
    <h2 class="mb-4">My Page — Purchased Items</h2>
    <#if none?? && none>
        <p class="text-center">You haven't bought anything yet.</p>
    <#else>
        <div class="row">
            <#list history as item>
                <div class="col-md-4 mb-4">
                    <div class="card h-100 text-center">
                        <img src="${item.image}" class="card-img-top" alt="${item.name}" style="height:200px; object-fit:contain;">
                        <div class="card-body">
                            <h5 class="card-title">${item.name}</h5>
                            <p class="card-text">Price: ₩${item.price}</p>
                        </div>
                    </div>
                </div>
            </#list>
        </div>
    </#if>
    <a href="/" class="btn btn-secondary mt-3">Continue Shopping</a>
</div>
</body>
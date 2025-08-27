<#assign currentPage = "shop">
<#include "common/header.ftl">
<body class="bg-light">
<div class="container">
    <div class="row">
        <#list items as item>
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">${item.name}</h5>
                        <img src="${item.image}" class="card-img-top" alt="${item.name}">
                        <p class="card-text">Price: ₩${item.price}</p>
                        <a href="/purchase?id=${item.id}" class="btn btn-primary">Buy</a>
                    </div>
                </div>
            </div>
        </#list>
    </div>
</div>
</body>
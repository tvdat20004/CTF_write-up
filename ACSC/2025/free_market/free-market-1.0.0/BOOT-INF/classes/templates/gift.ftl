<#include "common/header.ftl">
<body class="container py-4">
<h2>🎁 Gift Message Preview</h2>
<form method="post" action="/gift" class="mb-4">
  <div class="mb-3">
    <label for="message" class="form-label">Your Message</label>
    <textarea id="message" name="message" class="form-control" rows="4">${message!}</textarea>
  </div>
  <button type="submit" class="btn btn-success">Preview</button>
</form>
<#if preview??>
  <hr/>
  <h4>Rendered Output</h4>
  <div class="border p-3">${preview}</div>
</#if>
<a href="/" class="btn btn-secondary mt-3">Back to Shop</a>
</body>
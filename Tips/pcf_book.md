## Doamin User
```
javascript:(function(){
  const rows = document.querySelectorAll("table tbody tr");
  const results = [];
  rows.forEach(row => {
    const cols = row.querySelectorAll("td");
    if (!cols.length) return;
    const login = cols[0].innerText.trim();
    const comment = cols[3].innerText.trim();
    if (comment === "Domain") {
      results.push(login);
    }
  });

  const text = results.join("\n");
  navigator.clipboard.writeText(text);

  alert("Domain User:\n" + text);
})();

```

## Doamin Password
```
javascript:(function(){
  const rows = document.querySelectorAll("table tbody tr");
  const results = [];
  rows.forEach(row => {
    const cols = row.querySelectorAll("td");
    if (!cols.length) return;
    const password = cols[2].innerText.trim();
    const comment = cols[3].innerText.trim();
    if (comment === "Domain") {
      results.push(password);
    }
  });

  const text = results.join("\n");
  navigator.clipboard.writeText(text);

  alert("Domain Password:\n" + text);
})();

```

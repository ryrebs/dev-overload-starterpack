## Sample go basic web app

Run the app with `go run wiki.go`

Specifications:

1. Reads the content of a file from `data` folder and display it as a response

```
func viewHandler(w http.ResponseWriter, r *http.Request, title string) {
	p, err := loadPage(title)
	if err != nil {
		http.Redirect(w, r, "/edit/"+title, http.StatusFound)
		return
	}
	renderTemplate(w, "view", p)
}
```

2. Save content as txt. The title comes from a part of the route `/save/title-here`.The file will reside on `data/title-here.txt`. A successful saved will redirect to `/view/title-here`

```
func saveHandler(w http.ResponseWriter, r *http.Request, title string) {
	body := r.FormValue("body")
	p := &page{Title: title, Body: []byte(body)}
	err := p.save()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	http.Redirect(w, r, "/view/"+title, http.StatusFound)
}
```

3. View the saved data. `/view/title-here` .If data is not found redirect to edit.

```
func viewHandler(w http.ResponseWriter, r *http.Request, title string) {
	p, err := loadPage(title)
	if err != nil {
		http.Redirect(w, r, "/edit/"+title, http.StatusFound)
		return
	}
	renderTemplate(w, "view", p)
}
```

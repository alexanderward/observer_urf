import { HttpClient } from '@angular/common/http';
import { isNull } from 'util';
import { of } from 'rxjs';
import { environment } from 'src/environments/environment';

export abstract class HTTPBase {

    url = environment.url;
    constructor(private http: HttpClient, path) {
        this.url = `${this.url}/${path}`;
    }

    private buildUrl(path: string, queryStrings: {} = null) {
        if (isNull(path)) {
            path = '';
        }
        let url = `${this.url}/${path}`;
        if (!isNull(queryStrings)) {
            let qs = [];
            Object.keys(queryStrings).forEach(key => {
                qs.push(`${key}=${queryStrings[key]}`)
            })
            if (qs.length) {
                url = `${url}?` + qs.join('&');
            }

        }
        return url;
    }

    protected get(path: string = null, queryStrings: {} = null, external = false) {
        let fqdn;
        if (!external) {
            fqdn = this.buildUrl(path, queryStrings);
        } else {
            fqdn = path;
        }

        return this.http.get(fqdn);
    }

    protected post(path: string, data = {}) {
        const fqdn = this.buildUrl(path);
        return this.http.post(fqdn, data);
    }

    protected put(path: string, data = {}) {
        const fqdn = this.buildUrl(path);
        return this.http.put(fqdn, data);
    }

    protected delete(path) {
        const fqdn = this.buildUrl(path);
        return this.http.delete(fqdn);
    }
}
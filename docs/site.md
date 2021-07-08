# Web Site

## Editing Datafiles

* `config.yml` has configuration options.
* All data files are in `sitedata/`.

## Running locallly

In console:

```console
$ make run
```

and then open <http://localhost:5000>.

## Deploy

```console
$ make freeze
# verify no errors happen
$ make deploy
# pldi21.org updated ~30 seconds later
```

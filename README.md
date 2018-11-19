# Ebay prices
Search on [ebay](ebay.co.uk) auctions for sold prices and available auctions for sniping on [gixen](gixen.com)

### Example:

```
$ eprices amazon echo show
*£60.00 + £0.00    2018-12-04 Tuesday 264023436404 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-Locked-Activation-/264023436404
 £70.00 + £0.00    2018-11-25 Sunday 183542145782 http://www.ebay.co.uk/itm/Amazon-Echo-Connect-Making-Receiving-Phone-Calls-Your-Echo-Dot-Echo-Show-/183542145782
*£95.00 + £3.45    2018-12-19 Wednesday 183543666908 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-/183543666908
...
Recently Sold:
*£110.00 + £6.95 - Monday 2018-11-19 253988429725 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-NEW-Seals-intact-/253988429725
 £102.01 + £3.95 - Sunday 2018-11-18 123496858412 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-Mint-Condition-Original-Box-unmark-/123496858412
...

Available Auctions:
 £67.00 + £3.45 - Wednesday 2018-11-21 143018389819 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-/143018389819
*£117.00 + £9.00 - Wednesday 2018-11-21 113373025063 http://www.ebay.co.uk/itm/Amazon-Echo-Show-Smart-Assistant-Black-NO-RESERVE-/113373025063
...
```

## Installing to the pyenv 'tools3'

**Installation**

```
pyenv activate tools3
pip install .
pyenv deactivate
sudo cp ebay.yaml /etc
```

**Uninstalling**

```
pyenv activate tools3
pip uninstall eprices
pyenv deactivate
```

**Development**

```
pyenv virtualenv 3.6.0 ebay
pyenv local ebay
pip install -r requirements.txt
sudo cp ebay.yaml /etc
```
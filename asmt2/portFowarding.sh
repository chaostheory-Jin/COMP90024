#!/bin/bash

kubectl port-forward service/router -n fission 9090:80
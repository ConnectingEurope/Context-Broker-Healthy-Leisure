# Context Broker Healthy Leisure

![License](https://img.shields.io/github/license/ConnectingEurope/Context-Broker-Data-Visualisation)
![NGSI LD](https://img.shields.io/badge/NGSI-LD-red.svg)

**Please note that support questions will not be monitored during the summer period of July and August. **

The **Context Broker Healthy Leisure** is a **project** made up of different components that help public organisations monitor the state of their cities and recommend different leisure options based on the data collected. The project has two components:

- **Context Broker Healthy Leisure web component**. This component allows city councils and deputations to have a real-time and historical view of leisure data. It provides the following features:

    - **Real-time data** visualisation through geo-localised sensors on a map, based on the information from the **Orion LD Context Broker**.

    - **Historical data** visualisation for the sensors in table and graph formats, taking advantage of historical data tools like **Kibana**.

    - Easy **Configuration page** for the integration with the Context Broker.

    - **Rule engine** component to configure rules and thresholds to generate alerts.

    - **Analytical algorithms** to calculate the most used indexes in Healthy Leisure.

    - Deployment in **local environments**, **cloud environments** or **FIWARE lab** (Sandbox).

    For more information, read the [Objective](#objective) section.

    For the visualisation layer, the [Context Broker Data Visualisation Enabler](https://github.com/ConnectingEurope/Context-Broker-Data-Visualisation) has been reused, which has been adapted to be compatible with NGSI-LD. The Context Broker Data Visualisation is a [CEF Generic Enabler](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/CEF+Enablers).

    You can find more info at the [FIWARE developers](https://developers.fiware.org/) website and the [FIWARE](https://fiware.org/) website.

    The complete list of FIWARE GEs and Incubated FIWARE GEs can be found at the [FIWARE Catalogue](https://www.fiware.org/developers/catalogue/).

- **Context Broker Healthy Leisure citizen app**. This component is designed so that citizens can see the leisure options of the city based on their preferences, as well as see the realtime data.

**Context Broker Healthy Leisure web component** 
| :books: [User manual](project/doc/user/index.md) | :books: [Deployment manual](project/doc/tutorials/index.md) | :books: [Technical manual](project/doc/technical/index.md) |

**Context Broker Healthy Leisure citizen app**
| :books: [User manual](citizen_app/doc/user/index.md) | :books: [Deployment manual](citizen_app/doc/tutorials/index.md) | :books: [Technical manual](citizen_app/doc/technical/index.md) |

## Content

- [Objective](#objective)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Reference documentation](#reference-documentation)
- [License](#license)
- [Contributors](#contributors)

## Objective

The Context Broker Healthy Leisure was created with the aim of:

- Facilitating the **adoption** of the Context Broker.

- Helping cities and regions to monitor the environment and recommend healthy leisure activities.

- Give a tool to residents and tourists so that they can learn about the city's leisure options.

- Creating a solution that could be **reused in smart city and smart region projects**.

It could also be adapted to the needs of different users by developing its own features, taking advantage of the base of the solution. More information can be found in the [documentation](#documentation) section.

[Top](#context-broker-healthy-leisure)

## Documentation

The documentation of the **Context Broker Healthy Leisure web component** is available in the following [link](project/doc/index.md).

The documentation of the **Context Broker Healthy Leisure citizen app** is available in the following [link](citizen_app/doc/index.md).

[Top](#context-broker-healthy-leisure)

## Deployment

The deployment of the Context Broker Healthy Leisure web component, in a local environment, cloud environment or in [FIWARE lab](https://www.fiware.org/developers/fiware-lab/) can be found in the following [link](project/doc/tutorials/index.md).

[Top](#context-broker-healthy-leisure)

## Reference documentation

The following documentation is recommended to be read before starting to use the Context Broker Healthy Leisure:

- [Orion LD Context Broker](https://github.com/FIWARE/context.Orion-LD)
- [Smart data models](https://smartdatamodels.org)
- [FIWARE lab](https://www.fiware.org/developers/fiware-lab/)
- [NGSI LD specifications](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf)
- [NGSI LD step by step](https://ngsi-ld-tutorials.readthedocs.io/en/latest/)

[Top](#context-broker-healthy-leisure)

## License

Context Broker Healthy Leisure is licensed under [European Union Public License v1.2](LICENSE).

[Top](#context-broker-healthy-leisure)

## Contributors

The Context Broker Healthy Leisure has been carried out by:

- [CEF Digital](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/CEF+Digital+Home)
- [everis](https://www.everis.com/)
- [FIWARE](https://www.fiware.org/)

[Top](#context-broker-healthy-leisure)

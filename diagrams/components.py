"""Diagram generator for component design"""

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.network import Nginx
from diagrams.generic.network import Switch
from diagrams.programming.language import Python
from diagrams.onprem.client import Client
from diagrams.onprem.iac import Ansible
from diagrams.custom import Custom
from pathlib import Path

# Gradient definitions:
grad1_start = "#E57000"
grad1_end = "#050305"
gradient1 = f"{grad1_start}:{grad1_end}"
grad2_start = "#FAEF56"
grad2_end = "#D6E0E8"
gradient2 = f"{grad2_start}:{grad2_end}"
grad3_start = "#439706"
grad3_end = "#A9DB5E"
gradient3 = f"{grad3_start}:{grad3_end}"
grad4_start = "#EB3A69"
grad4_end = "#F3D9F3"
gradient4 = f"{grad4_start}:{grad4_end}"
grad5_start = "#00E2AA"
grad5_end = "#B4E6F4"
gradient5 = f"{grad5_start}:{grad5_end}"

# Heading sizes
heading1 = "45"
heading2 = "40"
heading3 = "20"
heading4 = "15"


# Cluster (Group) attributes:
proxmox_cluster_attributes: dict[str, str] = {
    "fontcolor": "#FFFFFF",
    "fontsize": heading2,
    "labeljust": "c",
    "margin": "35",
    "style": "filled",
    "fillcolor": gradient1,
    "gradientangle": "45",
}
home_assistant_cluster_attributes: dict[str, str] = {
    "fontcolor": "#000000",
    "fontsize": heading3,
    "labeljust": "c",
    "margin": "35",
    "style": "filled",
    "fillcolor": gradient2,
    "gradientangle": "270",
}
k3s_cluster_attributes: dict[str, str] = {
    "fontsize": heading3,
    "labeljust": "c",
    "margin": "35",
    "style": "filled",
    "fillcolor": gradient3,
    "gradientangle": "270",
}
awx_cluster_attributes: dict[str, str] = {"fontcolor": "#000000", "fontsize": heading3, "labeljust": "c", "style": "filled", "fillcolor": "#dddddd"}
python_cluster_attributes: dict[str, str] = {"fontcolor": "#000000", "fontsize": heading3, "labeljust": "c", "style": "filled", "fillcolor": "#dddddd"}
ingress_cluster_attributes: dict[str, str] = {"fontcolor": "#000000", "fontsize": heading3, "labeljust": "c", "style": "filled", "fillcolor": "#dddddd"}
interaction_cluster_attributes: dict[str, str] = {
    "fontsize": heading3,
    "labeljust": "c",
    "margin": "35",
    "style": "filled",
    "fillcolor": gradient4,
    "gradientangle": "270",
}
network_cluster_attributes: dict[str, str] = {
    "fontsize": heading3,
    "labeljust": "c",
    "margin": "35",
    "style": "filled",
    "fillcolor": gradient5,
    "gradientangle": "270",
}
# Node attributes
node_attributes = {
    "fontcolor": "#000000",
    "fontsize": heading4,
    "imagescale": "true",
}

with Diagram(
    "Time-Managed Internet Access Architecture",
    show=False,
    filename="./diagrams/Time_MGMT_Components",
    direction="LR",
    outformat="png",
    graph_attr={"bgcolor": "#B9B9B9", "fontsize": heading2},
    edge_attr={"penwidth": "3.0", "color": "#242323"},
):
    with Cluster("ProxMox VE", graph_attr=proxmox_cluster_attributes):
        # Home Assistant Block
        with Cluster("Home Assistant", graph_attr=home_assistant_cluster_attributes):
            home_assistant = Custom("Home Assistant", str(Path("./diagrams/symbols/ha.png").absolute()), **node_attributes)
            scheduler = Custom("Scheduler (06:00)", str(Path("./diagrams/symbols/ha_automation.png").absolute()), **node_attributes)
            input_button = Custom("Input Button\n(Press)", str(Path("./diagrams/symbols/ha_input_button.png").absolute()), **node_attributes)
            nodered_flow = Custom("NodeRED Flow", str(Path("./diagrams/symbols/node_red.png").absolute()), **node_attributes)

            home_assistant >> scheduler >> input_button >> Edge(label="Watch for\nPress Event", fontsize=heading3) >> nodered_flow

        # Kubernetes k3s Cluster
        with Cluster("Kubernetes k3s Cluster", graph_attr=k3s_cluster_attributes):
            with Cluster("K3s Ingress", graph_attr=ingress_cluster_attributes):
                nginx = Nginx("NGINX Ingress\nController", **node_attributes)

            # Ansible AWX Block
            with Cluster("Ansible AWX", graph_attr=awx_cluster_attributes):
                template = Ansible("Template:\nSet Switchport Status", **node_attributes)
                playbook = Ansible("Playbook:\nset-port-admin-status", **node_attributes)
                template >> playbook
                nginx >> template

            with Cluster("Python Workloads", graph_attr=python_cluster_attributes):
                # FastAPI Block
                fastapi = Python("FastAPI Python App\n(Time-MGMT REST API)", **node_attributes)
                nginx >> fastapi
                fastapi >> nginx

        nodered_flow >> nginx

    internet = Custom("Internet", str(Path("./diagrams/symbols/internet.png").absolute()), **node_attributes)
    internet >> nginx

    with Cluster("Interaction", graph_attr=interaction_cluster_attributes):
        # Swagger-UI
        swagger_ui = Custom("Remote MGMT\nSwagger UI", str(Path("./diagrams/symbols/swagger.png").absolute()), **node_attributes)
        swagger_ui >> Edge(label="HTTPS", fontsize=heading3) >> internet

        # Remote Display Interface
        remote_display = Custom("Remote Display\nInterface", str(Path("./diagrams/symbols/remote.png").absolute()), **node_attributes)
        remote_display >> Edge(xlabel="REST/HTTPS", label=" " * 23, fontsize=heading3) >> internet

    with Cluster("Network", graph_attr=network_cluster_attributes):
        # Access Switch and Endpoints
        access_switch = Switch("Access Switch", **node_attributes)
        playbook >> Edge(xlabel="SSH", label=" " * 40, fontsize=heading3) >> access_switch

        pc = Client("Target PC", **node_attributes)
        access_switch - pc

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.gcp.network import CDN, DNS, LoadBalancing, Armor, VPC, VPN
from diagrams.gcp.compute import KubernetesEngine
from diagrams.gcp.storage import Filestore, Storage
from diagrams.gcp.database import Firestore, SQL, Memorystore
from diagrams.gcp.security import Iam, KeyManagementService, SecurityCommandCenter
from diagrams.gcp.operations import Monitoring
from diagrams.generic.blank import Blank
from diagrams.generic.place import Datacenter
graph_attr = {
    "fontsize": "30",
}
compute_attr = {
    "bgcolor": "#6290C8",
}
vpc_attr = {
    "bgcolor": "#9381FF",
}
white_attr = {
    "bgcolor": "white",
}
blue_attr = {
    "bgcolor": "#BFDBF7",
}
lightgreen_attr = {
    "bgcolor": "#ACECA1",
}
green_attr = {
    "bgcolor": "#9381FF",
}
blue2_attr = {
    "bgcolor": "#A6B1E1",
}
green2_attr = {
    "bgcolor": "#B0BC98",
}
white_attr = {
    "height": "0.5",
}
cluster_attr = {
    "penwidth": "3",

}
with Diagram("general", show=False, graph_attr=graph_attr, direction="TB"):
    with Cluster("Clients", graph_attr=cluster_attr):
        client_white = Blank()
        client = [Client("Client"), Client("Client")]
    with Cluster("Networks", graph_attr=cluster_attr):
        network_white = Blank()
        cdn = CDN("cloud CDN")
        dns = DNS("Cloud DNS")
        armor = Armor("cloud Armor")
        loadBalancing = LoadBalancing("Cloud LoadBalancing")
        with Cluster("", direction="LR", graph_attr=vpc_attr):
            VPC("Share VPC Network")
            with Cluster("asia-east1", graph_attr=white_attr):
                with Cluster("subnet1", graph_attr=blue_attr):
                    asia_cluster1 = Blank()
                with Cluster("subnet2", graph_attr=lightgreen_attr):
                    asia_cluster2 = Blank()
                vpn = VPN("cloud VPN")

    with Cluster("Computes", graph_attr=cluster_attr):
        compute_white = Blank()
        with Cluster("subnet", graph_attr=compute_attr):
            GKE = KubernetesEngine("KubernetesEngine")

    with Cluster("Storages", graph_attr=cluster_attr):
        storage_white = Blank()
        with Cluster("Storage", graph_attr=blue2_attr):
            storage = Storage("Cloud Storage")
            filestore = Filestore("Filestore")

        with Cluster("Databases", graph_attr=blue2_attr):
            firestore = Firestore("Firesotre")
            with Cluster("subnet", graph_attr=green_attr):
                with Cluster("zone-a", graph_attr=blue_attr):
                    memorystore1 = Memorystore("Memorystore")
                    sql1 = SQL("PostgreSQL")
                with Cluster("zone-b", graph_attr=lightgreen_attr):
                    sql2 = SQL("PostgreSQL")
                    memorystore2 = Memorystore("Memorystore")

    with Cluster("Security&Monitoring", graph_attr=cluster_attr):
        security_white = Blank()
        with Cluster("Operation", graph_attr=green2_attr):
            monitoring = Monitoring("Monitoring")

        with Cluster("Security", graph_attr=green2_attr):
            iam = Iam("cloud Iam")
            keyManagementService = KeyManagementService("KeyManagementService")
            securityCommandCenter = SecurityCommandCenter(
                "cloud SecurityCommandCenter")

    with Cluster("On Premise", graph_attr=cluster_attr):
        onprise_white = Blank()
        datacenter = Datacenter("On Premise")

    # 排版
    client_white >> Edge(style="dotted", color="white") << network_white
    network_white >> Edge(style="dotted", color="white") << compute_white
    storage_white >> Edge(style="dotted", color="white") << onprise_white
    client_white >> Edge(style="dotted", color="white") << storage_white
    onprise_white >> Edge(style="dotted", color="white") << security_white

    client >> Edge(label="https", color="black") >> cdn
    cdn >> Edge(color="black") << loadBalancing
    dns >> Edge(color="black") >> loadBalancing
    loadBalancing - Edge(color="black") - armor
    loadBalancing >> Edge(color="black") >> GKE
    GKE >> Edge(label="https", color="black") >> storage
    GKE >> Edge(label="https", color="black") >> filestore
    GKE >> Edge(label="private service Access TLS", color="black") >> sql1
    GKE >> Edge(label="private service Access TLS",
                color="black") >> memorystore1
    sql1 >> Edge(color="black", label="Cloud SQL HA",
                 fontcolor="silver") << sql2
    memorystore1 >> Edge(color="black", label="Memorystore HA",
                         fontcolor="silver") << memorystore2
    GKE >> Edge(color="black") >> asia_cluster1
    sql1 >> Edge(color="black") >> asia_cluster2
    asia_cluster1 - Edge(color="black") - asia_cluster2
    asia_cluster2 >> Edge(color="black") >> vpn
    vpn >> Edge(color="black", label="IPsec") >> datacenter

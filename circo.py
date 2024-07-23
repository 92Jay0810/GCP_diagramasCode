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
    "layout": "circo",
    "oneblock": "true",
}
with Diagram("circo", show=False, graph_attr=graph_attr):
    client = [Client("Client"), Client("Client")]
    cdn = CDN("cloud CDN")
    dns = DNS("Cloud DNS")
    armor = Armor("cloud Armor")
    loadBalancing = LoadBalancing("Cloud LoadBalancing")
    VPC("Share VPC Network")
    asia_cluster1 = Blank("subnet1")
    asia_cluster2 = Blank("subnet2")
    vpn = VPN("cloud VPN")
    GKE = KubernetesEngine("KubernetesEngine")
    storage = Storage("Cloud Storage")
    filestore = Filestore("Filestore")
    firestore = Firestore("Firesotre")
    memorystore1 = Memorystore("Memorystore")
    sql1 = SQL("PostgreSQL")
    sql2 = SQL("PostgreSQL")
    memorystore2 = Memorystore("Memorystore")
    monitoring = Monitoring("Monitoring")
    iam = Iam("cloud Iam")
    keyManagementService = KeyManagementService("KeyManagementService")
    securityCommandCenter = SecurityCommandCenter(
        "cloud SecurityCommandCenter")
    Premise = Datacenter("On Premise")
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
    vpn >> Edge(color="black", label="IPsec") >> Premise

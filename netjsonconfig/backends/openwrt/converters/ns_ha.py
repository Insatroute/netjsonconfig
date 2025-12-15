from .base import OpenWrtConverter


def _uci_escape(v):
    if v is None:
        return ""
    # UCI uses single quotes; escape single quotes safely
    return str(v).replace("'", "'\\''")


class NsHa(OpenWrtConverter):
    """
    NetJSON key: ns_ha
    Output package: ns_ha  -> becomes /etc/config/ns_ha
    """

    netjson_key = "ns_ha"
    intermediate_key = "ns_ha"
    _uci_types = ["ns_ha"]

    def to_intermediate_loop(self, block, result, index=None):
        """
        Convert NetJSON ns_ha[0] -> intermediate UCI sections
        """
        if not block:
            return result

        # Your output expects: config ha 'settings'
        section_type = block.get("config_name", "ha")        # optional field
        section_name = block.get("config_value", "settings") # optional field

        section = {
            ".type": section_type,
            ".name": section_name,
        }

        # Map all other fields to UCI option keys
        skip = {"config_name", "config_value"}
        for k, v in block.items():
            if k in skip or v is None:
                continue
            section[k] = v

        result["ns_ha"] = [self.sorted_dict(section)]
        return result

    def to_netjson_loop(self, block, result, index):
        """
        Optional: convert UCI -> NetJSON (if you ever parse native configs).
        """
        # remove internal uci keys
        section_type = block.pop(".type", "ha")
        section_name = block.pop(".name", "settings")

        # restore into netjson format
        block["config_name"] = section_type
        block["config_value"] = section_name

        result.setdefault("ns_ha", [])
        result["ns_ha"].append(block)
        return result

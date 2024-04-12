lms_proto = Proto("LMSP", "LaMetric Stream Protocol")

lms_proto.fields.header = ProtoField.string("LMSP.header", "Header")
lms_proto.fields.session_id = ProtoField.bytes("LMSP.session_id", "Session ID")
lms_proto.fields.fixed = ProtoField.bytes("LMSP.Fixed", "Fixed Value")
lms_proto.fields.bytes = ProtoField.bytes("LMSP.bytes", "Byte array")
lms_proto.fields.colorsize = ProtoField.uint16("LMSP.color_size", "Color payload length")
lms_proto.fields.colorcode = ProtoField.bytes("LMSP.color_code", "Color payload")
lms_proto.fields.pixel_height = ProtoField.uint16("LMSP.pixel_height", "Height")
lms_proto.fields.pixel_width = ProtoField.uint16("LMSP.pixel_width", "Width")
lms_proto.fields.crc = ProtoField.bytes("LMSP.crc", "Checksum")

lms_proto.fields.unknown_byte = ProtoField.bytes("LaMetric.bytes", "Unknown Bytes")
lms_proto.fields.unknown_uin16 = ProtoField.int16("LaMetric.uint16", "Unknown UINT16")

function lms_proto.dissector(buffer, pinfo, tree)
  length = buffer:len()
  if length == 0 then return end

  pinfo.cols.protocol = lms_proto.name

  local lmsp_tree = tree:add(lms_proto, buffer(), "LaMetric Stream Data")

  lmsp_tree:add(lms_proto.fields.header, buffer(0, 4))                       -- __builtin_strncpy(buf_tosend, "lmsp", 4);
  lmsp_tree:add_le(lms_proto.fields.fixed, buffer(0x04, 2))                  -- *(uint16_t*)(buf_tosend + 4) = 1;
  lmsp_tree:add(lms_proto.fields.unknown_byte, buffer(0x05, 1))
  lmsp_tree:add(lms_proto.fields.session_id, buffer(0x06, 16))               -- strncpy(&buf_tosend[6], QByteArray::constData(((char*)r14 + 0x68)), _Count);
  lmsp_tree:add(lms_proto.fields.unknown_byte, buffer(0x16, 1))
  lmsp_tree:add_le(lms_proto.fields.fixed, buffer(0x17, 2))                  -- *(uint16_t*)(buf_tosend + 0x17) = 0x101;
  lmsp_tree:add_le(lms_proto.fields.fixed, buffer(0x1a, 4))                  -- *(uint32_t*)(buf_tosend + 0x1a) = 0;
  lmsp_tree:add_le(lms_proto.fields.pixel_width, buffer(0x1e, 2):le_uint())  -- *(buf_tosend + 0x1e) = rsi
  lmsp_tree:add_le(lms_proto.fields.pixel_height, buffer(0x20, 2):le_uint()) -- *(buf_tosend + 0x20) = rax_13
  lmsp_tree:add_le(lms_proto.fields.colorsize, buffer(0x22, 2):le_uint())    -- *(uint16_t*)(buf_tosend + 0x22) = ((int16_t)*(uint32_t*)((char*)colorarray + 4));
  local lmsp_colors = lmsp_tree:add(lms_proto, {}, "Color Data")
  for i = 0, length - 0x26 - 3, 3 do
    lmsp_colors:add(lms_proto.fields.colorcode, buffer(0x24 + i, 3))
  end
  lmsp_tree:add(lms_proto.fields.crc, buffer(length - 2, 2))
end

local udp_port = DissectorTable.get("udp.port")
udp_port:add(9999, lms_proto)
